from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework.response import Response
from rest_framework.views import APIView

from clothe.dto.clothe.clothe_input_dto import ClotheInputDto
from clothe.dto.clothe.clothe_output_dto import ClotheOutputDto
from clothe.models import Clothe


class ClotheController(APIView):
    id_param = openapi.Parameter('id', in_=openapi.IN_QUERY, description='Clothe ID', type=openapi.TYPE_NUMBER)
    category_id_param = openapi.Parameter('category_id', in_=openapi.IN_QUERY, description='Category ID',
                                          type=openapi.TYPE_NUMBER)

    @swagger_auto_schema(operation_description="Create a new clothe", request_body=ClotheInputDto,
                         responses={201: ClotheOutputDto})
    def post(self, request):
        data = ClotheInputDto(data=request.data)
        if data.is_valid():
            return Response(ClotheOutputDto(data.save()).data, status=201)
        else:
            return Response(data.errors, status=400)

    @swagger_auto_schema(operation_description="Get a clothe by ID or get all clothes",
                         manual_parameters=[id_param, category_id_param],
                         responses={200: ClotheOutputDto(many=True), 404: 'Not found'})
    def get(self, request):
        id = request.query_params.get('id')
        if id:
            try:
                clothe = Clothe.objects.get(id=id)
                data = ClotheOutputDto(clothe)
                return Response(data.data)
            except Clothe.DoesNotExist:
                return Response(status=404)
        else:
            category_id = request.query_params.get('category_id')
            clothes = Clothe.objects.filter(category_id=category_id) if category_id else Clothe.objects.all()
            data = ClotheOutputDto(clothes, many=True)
            return Response(data.data)

    @swagger_auto_schema(operation_description="Update a clothe by ID", manual_parameters=[id_param],
                         request_body=ClotheInputDto,
                         responses={200: ClotheOutputDto, 400: 'Bad Request'})
    def put(self, request):
        id = request.query_params.get('id')
        clothe = Clothe.objects.get(id=id)
        data = ClotheInputDto(instance=clothe, data=request.data)
        if data.is_valid():
            return Response(ClotheOutputDto(data.save()).data)
        else:
            return Response(data.errors, status=400)

    @swagger_auto_schema(operation_description="Delete a clothe by ID", manual_parameters=[id_param],
                         request_body=no_body,
                         responses={200: 'Success', 400: 'Bad Request'})
    def delete(self, request):
        id = request.query_params.get('id')
        clothe = Clothe.objects.get(id=id)
        clothe.delete()
        return Response(status=200)
