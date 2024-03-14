from django.urls import path

from clothe.controller.clothe_controller import ClotheController

urlpatterns = [
    path('clothes', ClotheController.as_view()),
]
