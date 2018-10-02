import factory
from factory.fuzzy import FuzzyInteger

from company.models import Company, Office


class CompanyFactory(factory.DjangoModelFactory):
    name = factory.Sequence(lambda n: 'company%d' % n)

    class Meta:
        model = Company


class OfficeFactory(factory.DjangoModelFactory):
    street = factory.Sequence(lambda n: 'Street%d' % n)
    postal_code = factory.Sequence(lambda n: 'Postal%d' % n)
    city = factory.Sequence(lambda n: 'City%d' % n)
    monthly_rent = FuzzyInteger(1000, 3000)
    company = factory.SubFactory(CompanyFactory)

    class Meta:
        model = Office
