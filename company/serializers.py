from rest_framework import serializers
from rest_framework.exceptions import NotFound

from company.models import Company, Office


class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = ('street', 'city', 'postal_code', 'headquarter')


class CompanySerializer(serializers.ModelSerializer):
    office = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ('name', 'office', 'total_monthly_rent')

    def get_office(self, obj):
        return OfficeSerializer(obj.office_set.all()[0]).data


class SetHeadquarterSerializer(serializers.Serializer):
    office_id = serializers.IntegerField(required=True)

    def validate(self, attrs):
        super(SetHeadquarterSerializer, self).validate(attrs)

        exists = Office.objects. \
            filter(id=attrs['office_id'],
                   company_id=self.context['company_id']). \
            exists()
        if not exists:
            raise NotFound()

        return attrs

    def save(self, **kwargs):
        Company.objects.set_head_quarter(
            company_id=kwargs['pk'],
            office_id=self.validated_data['office_id']
        )
