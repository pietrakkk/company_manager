# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from company.tests.factories import CompanyFactory, OfficeFactory


class CompanyViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.company1 = CompanyFactory()
        self.company1_headquarter = OfficeFactory(company=self.company1, headquarter=True)
        OfficeFactory(company=self.company1)

        self.company2 = CompanyFactory()
        self.company2_headquarter = OfficeFactory(company=self.company2, headquarter=True)
        OfficeFactory(company=self.company2)

    def test_company_list_view(self):
        response = self.client.get(reverse('company-list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        self.assertEqual(response.data[0]['name'], self.company1.name)
        self.assertEqual(response.data[0]['office']['city'], self.company1_headquarter.city)
        self.assertEqual(response.data[0]['office']['street'], self.company1_headquarter.street)
        self.assertEqual(response.data[0]['office']['postal_code'], self.company1_headquarter.postal_code)

        self.assertEqual(response.data[1]['name'], self.company2.name)
        self.assertEqual(response.data[1]['office']['city'], self.company2_headquarter.city)
        self.assertEqual(response.data[1]['office']['street'], self.company2_headquarter.street)
        self.assertEqual(response.data[1]['office']['postal_code'], self.company2_headquarter.postal_code)

    def test_company_offices_view(self):
        response = self.client.get(reverse('company-offices', args=[self.company1.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertTrue(response.data[0]['headquarter'])

    def test_not_existing_company_offices_view(self):
        not_existing_id = 1000
        response = self.client.get(reverse('company-offices', args=[not_existing_id]))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_set_company_headquarter_view(self):
        new_headquarter = OfficeFactory(company=self.company2)

        #  check actual headquarter
        response = self.client.get(reverse('company-detail', args=[self.company2.id]))

        self.assertEqual(response.data['office']['city'], self.company2_headquarter.city)
        self.assertEqual(response.data['office']['street'], self.company2_headquarter.street)
        self.assertEqual(response.data['office']['postal_code'], self.company2_headquarter.postal_code)

        #  change headquarter
        response = self.client.put(
            reverse('company-set-headquarter', args=[self.company2.id]),
            data={'office_id': new_headquarter.id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check if headquarter changed
        response = self.client.get(reverse('company-detail', args=[self.company2.id]))

        self.assertEqual(response.data['office']['city'], new_headquarter.city)
        self.assertEqual(response.data['office']['street'], new_headquarter.street)
        self.assertEqual(response.data['office']['postal_code'], new_headquarter.postal_code)

    def test_set_not_existing_company_headquarter_view(self):
        not_existing_id = 1000

        new_headquarter = OfficeFactory(company=self.company2)

        response = self.client.put(
            reverse('company-set-headquarter', args=[not_existing_id]),
            data={'office_id': new_headquarter.id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_set_not_existing_office_headquarter_view(self):
        not_existing_office_id = 32

        response = self.client.put(
            reverse('company-set-headquarter', args=[self.company2.id]),
            data={'office_id': not_existing_office_id}, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
