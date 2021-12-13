from serializers import FixtureSerializer


class Serializer(FixtureSerializer):
    def serialize(self, *args, **kwargs):
        return super(Serializer, self).serialize('json', *args, **kwargs)

    def deserialize(self, *args, **kwargs):
        return super(Serializer, self).deserialize('json', *args, **kwargs)

Deserializer = Serializer
