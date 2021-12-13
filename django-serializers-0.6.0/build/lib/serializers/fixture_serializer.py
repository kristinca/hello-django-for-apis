from django.core.serializers.base import DeserializedObject
from django.db import models
from django.utils.datastructures import SortedDict
from django.utils.encoding import smart_unicode
from serializers import Field, PrimaryKeyRelatedField, NaturalKeyRelatedField
from serializers import Serializer
from serializers.renderers import (
    JSONRenderer,
    YAMLRenderer,
    DumpDataXMLRenderer
)
from serializers.parsers import (
    JSONParser,
    DumpDataXMLParser
)
from serializers.utils import DictWithMetadata


class ModelNameField(Field):
    """
    Serializes the model instance's model name.  Eg. 'auth.User'.
    """
    def field_to_native(self, obj, field_name):
        return smart_unicode(obj._meta)

    def field_from_native(self, data, field_name, into):
        # We don't actually want to restore the model name metadata to a field.
        pass


class FixtureFields(Serializer):
    """
    A serializer which uses serializes all the local fields on a model.
    """

    # Use an unsorted dict to ensure byte-for-byte backwards compatability
    _dict_class = DictWithMetadata

    def default_fields(self, serialize, obj=None, data=None, nested=False):
        """
        Return the set of all fields defined on the model.
        For fixtures this consists of only the local fields on the model.
        """
        if serialize:
            cls = obj.__class__
        else:
            cls = self.parent.model

        # all local fields + all m2m fields without through relationship
        opts = cls._meta.concrete_model._meta
        fields = [field for field in opts.local_fields if field.serialize]
        fields += [field for field in opts.many_to_many
                   if field.serialize and field.rel.through._meta.auto_created]

        ret = SortedDict()
        for model_field in fields:
            if model_field.rel and nested:
                field = FixtureSerializer()
            elif model_field.rel:
                field = self._nk_or_pk_field(serialize, data, model_field)
            else:
                field = Field()
            field.initialize(parent=self, model_field=model_field)
            ret[model_field.name] = field
        return ret

    def _nk_or_pk_field(self, serialize, data, model_field):
        """
        Determine if natural key field or primary key field should be used.
        """
        if ((serialize and self.root.use_natural_keys) or
            not serialize
            and hasattr(model_field.rel.to._default_manager, 'get_by_natural_key')
            and hasattr(data[model_field.name], '__iter__')):
            return NaturalKeyRelatedField()
        return PrimaryKeyRelatedField()


class FixtureSerializer(Serializer):
    """
    A serializer that is used for serializing/deserializing fixtures.
    This is used by the 'dumpdata' and 'loaddata' managment commands.
    """

    # NB: Unsorted dict to ensure byte-for-byte backwards compatability
    _dict_class = DictWithMetadata

    pk = Field()
    model = ModelNameField()
    fields = FixtureFields(source='*')

    class Meta:
        renderer_classes = {
            'xml': DumpDataXMLRenderer,
            'json': JSONRenderer,
            'yaml': YAMLRenderer,
        }
        parser_classes = {
            'xml': DumpDataXMLParser,
            'json': JSONParser
        }

    def serialize(self, *args, **kwargs):
        """
        Override default behavior slightly:

        1. Add 'use_natural_keys' option to switch between PK and NK relations.
        2. The 'fields' and 'exclude' options should apply to the
           'FixtureFields' child serializer, not to the root serializer.
        """
        self.use_natural_keys = kwargs.pop('use_natural_keys', False)

        # TODO: Actually, this is buggy - fields/exclude will be retained as
        # state between subsequant calls to serialize()
        fields = kwargs.pop('fields', None)
        exclude = kwargs.pop('exclude', None)
        if fields is not None:
            self.fields['fields'].opts.fields = fields
        if exclude is not None:
            self.fields['fields'].opts.exclude = exclude

        return super(FixtureSerializer, self).serialize(*args, **kwargs)

    def restore_fields(self, data):
        """
        Prior to deserializing the fields, we want to determine the model
        class, and store it so it can be used to:

        1. Determine the correct fields for restoring attributes on the model.
        2. Determine the class to use when restoring the model.
        """
        self.model = models.get_model(*data['model'].split("."))
        return super(FixtureSerializer, self).restore_fields(data)

    def restore_object(self, attrs, instance=None):
        """
        Restore the model instance.
        """
        m2m_data = {}
        for field in self.model._meta.many_to_many:
            if field.name in attrs:
                m2m_data[field.name] = attrs.pop(field.name)
        return DeserializedObject(self.model(**attrs), m2m_data)
