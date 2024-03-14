from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from book.dto.book.book_input_dto import BookInputDto
from book.dto.book.book_output_dto import BookOutputDto
from book.models import Book


class BookController(APIView):
    id_param = openapi.Parameter('id', in_=openapi.IN_QUERY, description='ID of the book', type=openapi.TYPE_INTEGER)
    author_id_param = openapi.Parameter('author_id', in_=openapi.IN_QUERY, description='ID of the author',
                                        type=openapi.TYPE_INTEGER)
    publisher_ids_param = openapi.Parameter('publisher_ids', in_=openapi.IN_QUERY, description='IDs of the publishers',
                                            type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER))
    category_id_param = openapi.Parameter('category_id', in_=openapi.IN_QUERY, description='ID of the category',
                                          type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(operation_description="Create a new book", request_body=BookInputDto,
                         responses={201: BookOutputDto})
    def post(self, request: Request):
        data = BookInputDto(data=request.data)
        if data.is_valid():
            return Response(BookOutputDto(data.save()).data, status=201)
        else:
            return Response(data.errors, status=400)

    @swagger_auto_schema(operation_description="Get a book by ID or get all books",
                         manual_parameters=[id_param, author_id_param, publisher_ids_param, category_id_param],
                         responses={200: BookOutputDto(many=True), 404: 'Not found'})
    def get(self, request: Request):
        id = request.query_params.get('id')
        if id:
            try:
                book = Book.objects.get(id=id)
                data = BookOutputDto(book)
                return Response(data.data)
            except Book.DoesNotExist:
                return Response(status=404)
        else:
            author_id = request.query_params.get('author_id')
            publisher_ids = request.query_params.getlist('publisher_ids')
            category_id = request.query_params.get('category_id')
            books = Book.objects.filter(
                Q(author_id=author_id) if author_id else Q(),
                Q(publisherrefbook__publisher_id__in=publisher_ids) if publisher_ids else Q(),
                Q(category_id=category_id) if category_id else Q()
            )
            data = BookOutputDto(books, many=True)
            return Response(data.data)

    @swagger_auto_schema(operation_description="Update a book by ID", manual_parameters=[id_param],
                         request_body=BookInputDto, responses={200: BookOutputDto, 400: 'Bad Request'})
    def put(self, request: Request):
        id = request.query_params.get('id')
        book = Book.objects.get(id=id)
        data = BookInputDto(instance=book, data=request.data)
        if data.is_valid():
            return Response(BookOutputDto(data.update(book, data.validated_data)).data, status=200)
        else:
            return Response(data.errors, status=400)

    @swagger_auto_schema(operation_description="Delete a book by ID", manual_parameters=[id_param],
                         request_body=no_body, responses={204: 'No Content', 404: 'Not found'})
    def delete(self, request: Request):
        id = request.query_params.get('id')
        book = Book.objects.get(id=id)
        book.delete()
        return Response(status=204)
