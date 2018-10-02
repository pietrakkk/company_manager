from __future__ import unicode_literals

from django.db.models import Prefetch
from rest_framework.decorators import detail_route
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from company.models import Company, Office
from company.serializers import CompanySerializer, OfficeSerializer, SetHeadquarterSerializer


class CompanyListViewSet(ReadOnlyModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_queryset(self):

        if self.action == 'offices':
            return self.queryset.filter(id=self.kwargs['pk']). \
                prefetch_related('office_set')
        else:
            return self.queryset.prefetch_related(
                Prefetch('office_set',
                         queryset=Office.objects.filter(headquarter=True))
            )

    @detail_route(methods=['GET'])
    def offices(self, request: Request, pk: int) -> Response:
        company = self.get_object()
        serializer = OfficeSerializer(company.office_set, many=True)

        return Response(serializer.data)

    @detail_route(methods=['PUT'])
    def set_headquarter(self, request: Request, pk: int) -> Response:

        serializer = SetHeadquarterSerializer(data=request.data, context={'company_id': pk})
        serializer.is_valid(raise_exception=True)
        serializer.save(pk=pk)

        return Response()
