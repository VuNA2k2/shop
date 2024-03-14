from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from mobile.dto.mobile_input_dto import MobileInputDto
from mobile.dto.mobile_output_dto import MobileOutputDto
from mobile.models import Mobile


class MobileController(APIView):
    id_param = openapi.Parameter('id', in_=openapi.IN_QUERY, description='ID of the mobile', type=openapi.TYPE_INTEGER)
    category_id_param = openapi.Parameter('category_id', in_=openapi.IN_QUERY, description='ID of the category',
                                          type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(operation_description="Create a new mobile", request_body=MobileInputDto,
                         responses={201: MobileOutputDto})
    def post(self, request: Request):
        data = MobileInputDto(data=request.data)
        if data.is_valid():
            return Response(MobileOutputDto(data.save()).data, status=201)
        else:
            return Response(data.errors, status=400)

    @swagger_auto_schema(operation_description="Get a mobile by ID or get all mobiles",
                         manual_parameters=[id_param, category_id_param],
                         responses={200: MobileOutputDto(many=True), 404: 'Not found'})
    def get(self, request: Request):
        id = request.query_params.get('id')
        if id:
            try:
                mobile = Mobile.objects.get(id=id)
                data = MobileOutputDto(mobile)
                return Response(data.data)
            except Mobile.DoesNotExist:
                return Response(status=404)
        else:
            category_id = request.query_params.get('category_id')
            mobiles = Mobile.objects.filter(
                Q(category_id=category_id) if category_id else Q()
            )
            data = MobileOutputDto(mobiles, many=True)
            return Response(data.data)

    @swagger_auto_schema(operation_description="Update a mobile by ID", manual_parameters=[id_param],
                         request_body=MobileInputDto, responses={200: MobileOutputDto, 400: 'Bad Request'})
    def put(self, request: Request):
        id = request.query_params.get('id')
        mobile = Mobile.objects.get(id=id)
        data = MobileInputDto(instance=mobile, data=request.data)
        if data.is_valid():
            return Response(MobileOutputDto(data.update(mobile, data.validated_data)).data, status=200)
        else:
            return Response(data.errors, status=400)

    @swagger_auto_schema(operation_description="Delete a mobile by ID", manual_parameters=[id_param],
                         request_body=no_body, responses={204: 'No Content', 404: 'Not found'})
    def delete(self, request: Request):
        id = request.query_params.get('id')
        mobile = Mobile.objects.get(id=id)
        mobile.delete()
        return Response(status=204)
