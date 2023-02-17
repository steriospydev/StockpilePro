import factory

from apps.supplier.models import Supplier


class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplier

    company = factory.Faker("company")
    sku_num = factory.Faker("lexify", text="??", letters="abcdefghijklmnopqrstuvwxyz0123456789")
    address = factory.Faker("address")
    city = factory.Faker("city")
    area = factory.Faker("state")
    zipcode = factory.Faker("random_number", digits=5, fix_len=True)
    person = factory.Faker("name")
    phone = factory.Faker("random_number", digits=10, fix_len=True)
    email = factory.Faker("email")
    TIN_num = factory.Faker("numerify", text="#########")
    TIN_agency = factory.Faker("city")


