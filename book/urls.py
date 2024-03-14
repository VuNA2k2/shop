from django.urls import path

from book.controller.author_controller import AuthorController
from book.controller.book_controller import BookController
from book.controller.publisher_controller import PublisherController

urlpatterns = [
    path('books', BookController.as_view()),
    path('authors', AuthorController.as_view()),
    path('publishers', PublisherController.as_view()),
]
