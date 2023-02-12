import factory

from apps.supplier.models import Supplier, Quote, Address, TIN, Contact


class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplier

    company = factory.Faker("company")
    sku_num = factory.Faker("lexify", text="??", letters="abcdefghijklmnopqrstuvwxyz0123456789")

class QuoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Quote

    supplier = factory.SubFactory(SupplierFactory)
    quote = factory.Faker("text")
    type = factory.Iterator(['email', 'phone', 'text'])

class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    supplier = factory.SubFactory(SupplierFactory)
    address = factory.Faker("address")
    city = factory.Faker("city")
    area = factory.Faker("state")
    zipcode = factory.Faker("random_number", digits=5, fix_len=True)

class ContactFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contact

    supplier = factory.SubFactory(SupplierFactory)
    person = factory.Faker("name")
    phone = factory.Faker("random_number", digits=10, fix_len=True)
    email = factory.Faker("email")

class TINFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TIN

    supplier = factory.SubFactory(SupplierFactory)
    TIN_num = factory.Faker("numerify", text="#########")
    TIN_agency = factory.Faker("city")
