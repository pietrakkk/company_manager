# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, transaction
from django.db.models import Sum
from django.utils.functional import cached_property


class CompanyManager(models.Manager):

    @transaction.atomic
    def set_head_quarter(self, company_id: int, office_id: int):
        Office.objects.filter(company_id=company_id, headquarter=True).update(headquarter=False)
        Office.objects.filter(company_id=company_id, id=office_id).update(headquarter=True)


class Company(models.Model):
    objects = CompanyManager()

    name = models.CharField('Name', max_length=300)

    @cached_property
    def total_monthly_rent(self):
        total_sum =  Office.objects.\
            filter(company_id=self.id).\
            aggregate(Sum('monthly_rent'))

        return total_sum['monthly_rent__sum']


class Office(models.Model):
    street = models.CharField('Street', max_length=256, blank=True)
    postal_code = models.CharField('Postal Code', max_length=32, blank=True)
    city = models.CharField('City', max_length=128, blank=True, null=True)
    monthly_rent = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    headquarter = models.BooleanField(default=False)
