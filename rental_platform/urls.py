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
from django.urls import path

import user.views as user_views
import equipment.views as equipment_views
import application.rent_application.views as rent_application_views
import application.renter_application.views as renter_application_views
import application.release_application.views as release_application_views
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login', user_views.login),

    # user related
    path('api/v1/users/', user_views.UsersList.as_view()),
    path('api/v1/users/<int:pk>', user_views.UserDetail.as_view()),

    # equipments related
    path('api/v1/equipment', equipment_views.EquipmentList.as_view()),
    path('api/v1/equipment/<int:pk>', equipment_views.EquipmentDetail.as_view()),

    # application related

    path('api/v1/renter-application', renter_application_views.RenterApplicationList.as_view()),
    path('api/v1/renter-application/<int:pk>', renter_application_views.RenterApplicationDetail.as_view()),
    path('api/v1/renter-application/<int:pk>/approve', renter_application_views.RenterApplicationAccept.as_view()),
    path('api/v1/renter-application/<int:pk>/reject', renter_application_views.RenterApplicationReject.as_view()),

    path('api/v1/rent-application', rent_application_views.RentApplicationList.as_view()),
    path('api/v1/rent-application/<int:pk>', rent_application_views.RentApplicationDetail.as_view()),
    path('api/v1/rent-application/<int:pk>/approve', rent_application_views.RentApplicationAccept.as_view()),
    path('api/v1/rent-application/<int:pk>/reject', rent_application_views.RentApplicationReject.as_view()),

]
