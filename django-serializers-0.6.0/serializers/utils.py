# -*- coding: utf-8 -*-
from django.utils.datastructures import SortedDict
from django.utils.timezone import is_aware

import csv
import datetime
import decimal
import inspect
import types
from django.utils import simplejson as json


def is_simple_callable(obj):
    """
    True if the object is a callable that takes no arguments.
    """
    return (
        (inspect.isfunction(obj) and not inspect.getargspec(obj)[0]) or
        (inspect.ismethod(obj) and len(inspect.getargspec(obj)[0]) <= 1)
    )


class DictWithMetadata(dict):
    """
    A dict-like object, that can have additional metadata attached.
    """
    def __init__(self, *args, **kwargs):
        super(DictWithMetadata, self).__init__(*args, **kwargs)
        self.metadata = {}

    def set_with_metadata(self, key, value, metadata):
        self[key] = value
        self.metadata[key] = metadata

    def items_with_metadata(self):
        return [(key, value, self.metadata[key])
        for (key, value) in self.items()]


class SortedDictWithMetadata(SortedDict, DictWithMetadata):
    pass


try:
    import yaml
except ImportError:
    SafeDumper = None
else:
    # Adapted from http://pyyaml.org/attachment/ticket/161/use_ordered_dict.py
    class SafeDumper(yaml.SafeDumper):
        """
        Handles decimals as strings.
        Handles SortedDicts as usual dicts, but preserves field order, rather
        than the usual behaviour of sorting the keys.
        """
        def represent_decimal(self, data):
            return self.represent_scalar('tag:yaml.org,2002:str', str(data))

        def represent_mapping(self, tag, mapping, flow_style=None):
            value = []
            node = yaml.MappingNode(tag, value, flow_style=flow_style)
            if self.alias_key is not None:
                self.represented_objects[self.alias_key] = node
            best_style = True
            if hasattr(mapping, 'items'):
                mapping = list(mapping.items())
                if not isinstance(mapping, SortedDict):
                    mapping.sort()
            for item_key, item_value in mapping:
                node_key = self.represent_data(item_key)
                node_value = self.represent_data(item_value)
                if not (isinstance(node_key, yaml.ScalarNode) and not node_key.style):
                    best_style = False
                if not (isinstance(node_value, yaml.ScalarNode) and not node_value.style):
                    best_style = False
                value.append((node_key, node_value))
            if flow_style is None:
                if self.default_flow_style is not None:
                    node.flow_style = self.default_flow_style
                else:
                    node.flow_style = best_style
            return node

    SafeDumper.add_representer(DictWithMetadata,
            yaml.representer.SafeRepresenter.represent_dict)
    SafeDumper.add_representer(SortedDictWithMetadata,
            yaml.representer.SafeRepresenter.represent_dict)
    SafeDumper.add_representer(types.GeneratorType,
            yaml.representer.SafeRepresenter.represent_list)


class DjangoJSONEncoder(json.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time and decimal types.
    """
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, decimal.Decimal):
            return str(o)
        elif hasattr(o, '__iter__'):
            return [i for i in o]
        return super(DjangoJSONEncoder, self).default(o)


class DictWriter(csv.DictWriter):
    """
    >>> from cStringIO import StringIO
    >>> f = StringIO()
    >>> w = DictWriter(f, ['a', 'b'], restval=u'î')
    >>> w.writerow({'a':'1'})
    >>> w.writerow({'a':'1', 'b':u'ø'})
    >>> w.writerow({'a':u'é'})
    >>> f.seek(0)
    >>> r = DictReader(f, fieldnames=['a'], restkey='r')
    >>> r.next() == {'a':u'1', 'r':[u"î"]}
    True
    >>> r.next() == {'a':u'1', 'r':[u"ø"]}
    True
    >>> r.next() == {'a':u'é', 'r':[u"î"]}
    """
    def __init__(self, csvfile, fieldnames, restval='', extrasaction='raise', dialect='excel', encoding='utf-8', *args, **kwds):
        self.fieldnames = fieldnames
        self.encoding = encoding
        self.restval = restval
        self.writer = csv.DictWriter(csvfile, fieldnames, restval, extrasaction, dialect, *args, **kwds)

    def _stringify(self, s, encoding):
        if type(s) == unicode:
            return s.encode(encoding)
        elif isinstance(s, (int, float)):
            pass  # let csv.QUOTE_NONNUMERIC do its thing.
        elif type(s) != str:
            s = str(s)
        return s

    def writeheader(self):
        header = dict([(item, item) for item in self.fieldnames])
        self.writerow(header)

    def writerow(self, d):
        for fieldname in self.fieldnames:
            if fieldname in d:
                d[fieldname] = self._stringify(d[fieldname], self.encoding)
            else:
                d[fieldname] = self._stringify(self.restval, self.encoding)
        self.writer.writerow(d)
