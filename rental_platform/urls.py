"""rental_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView

from allauth.account.views import confirm_email
from rest_framework import routers
from rest_framework.schemas import get_schema_view



from user.views import UserViewSet
from equipment.views import EquipmentViewSet
from application.renter_application.views import RenterApplicationViewSet
from application.rent_application.views import RentApplicationViewSet
from application.release_application.views import ReleaseApplicationViewSet
from message.views import MessageViewSet
# from django.middleware.csrf import get_token
# from django.http import JsonResponse
#
#
# def get_scsrf(request):
#     csrf_token = get_token(request)
#     return JsonResponse({'token': csrf_token})


router = routers.SimpleRouter()
router.register(r'api/v1/user', UserViewSet)
router.register(r'api/v1/equipment', EquipmentViewSet)
router.register(r'api/v1/renter-application', RenterApplicationViewSet)
router.register(r'api/v1/rent-application', RentApplicationViewSet)
router.register(r'api/v1/release-application', ReleaseApplicationViewSet)
router.register(r'api/v1/message', MessageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/v1/rest-auth/', include('rest_auth.urls')),
    url(r'^api/v1/rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api/v1/accounts/', include('allauth.urls')),
    url(r'^api/v1/account-rest/registration/account-confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
    path('api/v1/swagger-ui/', TemplateView.as_view(template_name='swagger-ui.html',extra_context={'schema_url': 'openapi-schema'}), name='swagger-ui'),
    path('openapi', get_schema_view(
        title="Rental Platform",
        description="API for all things …",
        version="1.0.0"
    ), name='openapi-schema'),
]

urlpatterns += router.urls
