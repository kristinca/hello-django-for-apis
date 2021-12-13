import json
from xml.dom import pulldom
from django.core.serializers.base import DeserializationError


class JSONParser(object):
    def parse(self, stream):
        try:
            return json.load(stream)
        except Exception as e:
            # Map to deserializer error
            raise DeserializationError(e)


class DumpDataXMLParser(object):
    def parse(self, stream):
        event_stream = pulldom.parse(stream)
        for event, node in event_stream:
            if event == "START_ELEMENT" and node.nodeName == "object":
                event_stream.expandNode(node)
                yield self._handle_object(node)

    def _handle_object(self, node):
        ret = {}

        if node.hasAttribute("pk"):
            ret['pk'] = node.getAttribute('pk')
        else:
            ret['pk'] = None
        ret['model'] = node.getAttribute('model')

        fields = {}
        for field_node in node.getElementsByTagName("field"):
            # If the field is missing the name attribute, bail
            name = field_node.getAttribute("name")
            rel = field_node.getAttribute("rel")
            if not name:
                raise DeserializationError("<field> node is missing the 'name' attribute")

            if field_node.getElementsByTagName('None'):
                value = None
            elif rel == 'ManyToManyRel':
                value = [n.getAttribute('pk') for n in field_node.getElementsByTagName('object')]
            elif field_node.getElementsByTagName('natural'):
                value = [getInnerText(n).strip() for n in field_node.getElementsByTagName('natural')]
            else:
                value = getInnerText(field_node).strip()

            fields[name] = value

        ret['fields'] = fields

        return ret


def getInnerText(node):
    """
    Get all the inner text of a DOM node (recursively).
    """
    # inspired by http://mail.python.org/pipermail/xml-sig/2005-March/011022.html
    inner_text = []
    for child in node.childNodes:
        if child.nodeType == child.TEXT_NODE or child.nodeType == child.CDATA_SECTION_NODE:
            inner_text.append(child.data)
        elif child.nodeType == child.ELEMENT_NODE:
            inner_text.extend(getInnerText(child))
        else:
            pass
    return u"".join(inner_text)
