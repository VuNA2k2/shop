from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework.response import Response
from rest_framework.views import APIView

from category.dto.category.category_input_dto import CategoryInputDto
from category.dto.category.category_output_dto import CategoryOutputDto
from category.models import Category


class CategoryController(APIView):
    id_param = openapi.Parameter('id', in_=openapi.IN_QUERY, description='ID of the category',
                                 type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(operation_description="Create a new category", request_body=CategoryInputDto,
                         responses={201: CategoryOutputDto})
    def post(self, request):
        data = CategoryInputDto(data=request.data)
        if data.is_valid():
            return Response(CategoryOutputDto(data.save()).data, status=201)
        else:
            return Response(data.errors, status=400)

    @swagger_auto_schema(operation_description="Get a category by ID or get all categories",
                         manual_parameters=[id_param], responses={200: CategoryOutputDto(many=True), 404: 'Not found'})
    def get(self, request):
        id = request.query_params.get('id')
        if id:
            category = Category.objects.get(id=id)
            data = CategoryOutputDto(category)
            return Response(data.data)
        else:
            categories = Category.objects.all()
            data = CategoryOutputDto(categories, many=True)
            return Response(data.data)

    @swagger_auto_schema(operation_description="Update a category by ID", manual_parameters=[id_param],
                         request_body=CategoryInputDto, responses={200: CategoryOutputDto, 400: 'Bad Request'})
    def put(self, request):
        id = request.query_params.get('id')
        category = Category.objects.get(id=id)
        data = CategoryInputDto(instance=category, data=request.data)
        if data.is_valid():
            return Response(CategoryOutputDto(data.update(category, data.validated_data)).data, status=200)
        else:
            return Response(data.errors, status=400)

    @swagger_auto_schema(operation_description="Delete a category by ID", manual_parameters=[id_param],
                         request_body=no_body, responses={204: 'No Content', 404: 'Not found'})
    def delete(self, request):
        id = request.query_params.get('id')
        category = Category.objects.get(id=id)
        category.delete()
        return Response(status=204)
