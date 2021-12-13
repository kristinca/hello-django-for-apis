from serializers import FixtureSerializer


class Serializer(FixtureSerializer):
    def serialize(self, *args, **kwargs):
        return super(Serializer, self).serialize('xml', *args, **kwargs)

    def deserialize(self, *args, **kwargs):
        return super(Serializer, self).deserialize('xml', *args, **kwargs)

Deserializer = Serializer
