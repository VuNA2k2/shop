from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from book.dto.author.author_input_dto import AuthorInputDto
from book.dto.author.author_output_dto import AuthorOutputDto
from book.models import Author


class AuthorController(APIView):
    id_param = openapi.Parameter('id', in_=openapi.IN_QUERY, description='ID of the author', type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(operation_description="Create a new author", request_body=AuthorInputDto,
                         responses={201: AuthorOutputDto})
    def post(self, request: Request):
        data = AuthorInputDto(data=request.data)
        if data.is_valid():
            return Response(AuthorOutputDto(data.save()).data, status=201)
        else:
            return Response(data.errors, status=400)

    @swagger_auto_schema(operation_description="Get an author by ID or get all authors", manual_parameters=[id_param],
                         responses={200: AuthorOutputDto(many=True), 404: 'Not found'})
    def get(self, request: Request):
        id = request.query_params.get('id')
        if id:
            author = Author.objects.get(id=id)
            data = AuthorOutputDto(author)
            return Response(data.data)
        else:
            authors = Author.objects.all()
            data = AuthorOutputDto(authors, many=True)
            return Response(data.data)

    @swagger_auto_schema(operation_description="Update an author by ID", manual_parameters=[id_param],
                         request_body=AuthorInputDto, responses={200: AuthorOutputDto, 400: 'Bad Request'})
    def put(self, request: Request):
        id = request.query_params.get('id')
        author = Author.objects.get(id=id)
        data = AuthorInputDto(instance=author, data=request.data)
        if data.is_valid():
            return Response(AuthorOutputDto(data.update(author, data.validated_data)).data, status=200)
        else:
            return Response(data.errors, status=400)

    @swagger_auto_schema(operation_description="Delete an author by ID", manual_parameters=[id_param],
                         request_body=no_body, responses={204: 'No Content', 404: 'Not found'})
    def delete(self, request: Request):
        id = request.query_params.get('id')
        author = Author.objects.get(id=id)
        author.delete()
        return Response(status=204)
