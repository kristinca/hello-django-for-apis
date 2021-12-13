from serializers import FixtureSerializer


class Serializer(FixtureSerializer):
    def serialize(self, *args, **kwargs):
        return super(Serializer, self).serialize('yaml', *args, **kwargs)

    def deserialize(self, *args, **kwargs):
        return super(Serializer, self).deserialize('yaml', *args, **kwargs)

Deserializer = Serializer
