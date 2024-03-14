from category.controller.category_controller import CategoryController
from django.urls import path

urlpatterns = [
    path('categories', CategoryController.as_view(), name='category'),
]