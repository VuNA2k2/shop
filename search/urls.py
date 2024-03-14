from django.urls import path

from search.search_controller import BookSearchController, MobileSearchController, ClotheSearchController

urlpatterns = [
    path('books', BookSearchController.as_view(), name='search'),
    path('mobiles', MobileSearchController.as_view(), name='search'),
    path('clothes', ClotheSearchController.as_view(), name='search'),
]
