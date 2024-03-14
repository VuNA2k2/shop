from django.urls import path

from mobile.controller.mobile_controller import MobileController

urlpatterns = [
    path('mobiles', MobileController.as_view(), name='mobile'),
]
