import datetime
from django.utils import simplejson as json
from django.utils.encoding import smart_unicode
from django.utils.html import urlize
from django.utils.xmlutils import SimplerXMLGenerator
from serializers.utils import SafeDumper, DictWriter, DjangoJSONEncoder
try:
    import yaml
except ImportError:
    yaml = None


class BaseRenderer(object):
    """
    Defines the base interface that renderers should implement.
    """

    def render(obj, stream, **opts):
        return str(obj)


class JSONRenderer(BaseRenderer):
    """
    Render a native python object into JSON.
    """
    def render(self, obj, stream, **opts):
        indent = opts.pop('indent', None)
        sort_keys = opts.pop('sort_keys', False)
        return json.dump(obj, stream, cls=DjangoJSONEncoder,
                         indent=indent, sort_keys=sort_keys)


class YAMLRenderer(BaseRenderer):
    """
    Render a native python object into YAML.
    """
    def render(self, obj, stream, **opts):
        indent = opts.pop('indent', None)
        default_flow_style = opts.pop('default_flow_style', None)
        return yaml.dump(obj, stream, Dumper=SafeDumper,
                         indent=indent, default_flow_style=default_flow_style)


class HTMLRenderer(BaseRenderer):
    """
    A basic html renderer, that renders data into tabular format.
    """
    def render(self, obj, stream, **opts):
        self._to_html(stream, obj)

    def _to_html(self, stream, data):
        if isinstance(data, dict):
            stream.write('<table>\n')
            for key, value in data.items():
                stream.write('<tr><td>%s</td><td>' % key)
                self._to_html(stream, value)
                stream.write('</td></tr>\n')
            stream.write('</table>\n')

        elif hasattr(data, '__iter__'):
            stream.write('<ul>\n')
            for item in data:
                stream.write('<li>')
                self._to_html(stream, item)
                stream.write('</li>')
            stream.write('</ul>\n')

        else:
            stream.write(urlize(smart_unicode(data)))


class XMLRenderer(BaseRenderer):
    """
    Render a native python object into a generic XML format.
    """
    def render(self, obj, stream, **opts):
        xml = SimplerXMLGenerator(stream, 'utf-8')
        xml.startDocument()
        self._to_xml(xml, obj)
        xml.endDocument()

    def _to_xml(self, xml, data):
        if isinstance(data, dict):
            xml.startElement('object', {})
            for key, value in data.items():
                xml.startElement(key, {})
                self._to_xml(xml, value)
                xml.endElement(key)
            xml.endElement('object')

        elif hasattr(data, '__iter__'):
            xml.startElement('list', {})
            for item in data:
                xml.startElement('item', {})
                self._to_xml(xml, item)
                xml.endElement('item')
            xml.endElement('list')

        else:
            xml.characters(smart_unicode(data))


class DumpDataXMLRenderer(BaseRenderer):
    """
    Render a native python object into XML dumpdata format.
    """
    def render(self, obj, stream, **opts):
        xml = SimplerXMLGenerator(stream, 'utf-8')
        xml.startDocument()
        xml.startElement('django-objects', {'version': '1.0'})
        if hasattr(obj, '__iter__'):
            [self.model_to_xml(xml, item) for item in obj]
        else:
            self.model_to_xml(xml, obj)
        xml.endElement('django-objects')
        xml.endDocument()

    def model_to_xml(self, xml, data):
        pk = data['pk']
        model = data['model']
        fields = data['fields']

        attrs = {}
        if pk is not None:
            attrs['pk'] = unicode(pk)
        attrs['model'] = model

        xml.startElement('object', attrs)

        # Due to implmentation details, the existing xml dumpdata format
        # renders ordered fields, whilst json and yaml render unordered
        # fields (ordering determined by python's `dict` implementation)
        # To maintain byte-for-byte backwards compatability,
        # we'll deal with that now.
        sorted_items = sorted(fields.items_with_metadata(),
                              key=lambda x: x[2].creation_counter)

        for key, value, field in sorted_items:
            attrs = {'name': key}
            attrs.update(field.attributes())
            xml.startElement('field', attrs)

            if value is not None and getattr(field, 'is_natural_key', False):
                self.handle_natural_key(xml, value)
            elif attrs.get('rel', None) == 'ManyToManyRel':
                self.handle_many_to_many(xml, value)
            elif isinstance(value, (datetime.datetime, datetime.date, datetime.time)):
                self.handle_datetimes(xml, value)
            elif value is None:
                self.handle_none(xml)
            else:
                self.handle_value(xml, value)

            xml.endElement('field')
        xml.endElement('object')

    def handle_natural_key(self, xml, value):
        for item in value:
            xml.addQuickElement('natural', contents=item)

    def handle_many_to_many(self, xml, value):
        for item in value:
            xml.addQuickElement('object', attrs={'pk': str(item)})

    def handle_datetimes(self, xml, value):
        xml.characters(value.isoformat())

    def handle_value(self, xml, value):
        xml.characters(smart_unicode(value))

    def handle_none(self, xml):
        xml.addQuickElement('None')


class CSVRenderer(BaseRenderer):
    def render(self, obj, stream, **opts):
        if isinstance(obj, dict) or not hasattr(obj, '__iter__'):
            obj = [obj]
        writer = None
        for item in obj:
            if not writer:
                writer = DictWriter(stream, item.keys())
                writer.writeheader()
            writer.writerow(item)

if not yaml:
    YAMLRenderer = None
