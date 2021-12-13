from serializers import FixtureSerializer


class Serializer(FixtureSerializer):
    internal_use_only = True  # Backwards compatability

    def serialize(self, *args, **kwargs):
        return super(Serializer, self).serialize('python', *args, **kwargs)

    def deserialize(self, *args, **kwargs):
        return super(Serializer, self).deserialize('python', *args, **kwargs)

Deserializer = Serializer
