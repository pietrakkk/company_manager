from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from company.views import CompanyListViewSet

router = DefaultRouter()
router.register(r'companies', CompanyListViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
]
