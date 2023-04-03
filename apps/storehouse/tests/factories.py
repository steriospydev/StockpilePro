import factory
from apps.storehouse.models import Storage, Section, Spot, Bin, BinType

class StorageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Storage

    storage_name = factory.Faker('pystr', max_chars=1)
    capacity = factory.Faker('sentence')
    location = factory.Faker('address')
    summary = factory.Faker('text')


class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Section

    section_name = factory.Faker('pystr', max_chars=1)


class SpotFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Spot

    spot_name = factory.Sequence(lambda n: f"{n+1:03}")


class BinFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bin

    storage = factory.SubFactory(StorageFactory)
    section = factory.SubFactory(SectionFactory)
    spot = factory.SubFactory(SpotFactory)
    bin_type = factory.Iterator([BinType.SHELF, BinType.FLOOR])
    in_use = False
