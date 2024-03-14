from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg import openapi
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from book.dto.publisher.publisher_input_dto import PublisherInputDto
from book.dto.publisher.publisher_output_dto import PublisherOutputDto
from book.models import Publisher


class PublisherController(APIView):
    id_param = openapi.Parameter('id', in_=openapi.IN_QUERY, description='ID of the publisher',
                                 type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(operation_description="Create a new publisher", request_body=PublisherInputDto,
                         responses={201: PublisherOutputDto})
    def post(self, request: Request):
        data = PublisherInputDto(data=request.data)
        if data.is_valid():
            return Response(PublisherOutputDto(data.save()).data, status=201)
        else:
            return Response(data.errors, status=400)

    @swagger_auto_schema(operation_description="Get a publisher by ID or get all publishers",
                         manual_parameters=[id_param], responses={200: PublisherOutputDto(many=True), 404: 'Not found'})
    def get(self, request: Request):
        id = request.query_params.get('id')
        if id:
            try:
                publisher = Publisher.objects.get(id=id)
                data = PublisherOutputDto(publisher)
                return Response(data.data)
            except Publisher.DoesNotExist:
                return Response(status=404)
        else:
            publishers = Publisher.objects.all()
            data = PublisherOutputDto(publishers, many=True)
            return Response(data.data)

    @swagger_auto_schema(operation_description="Update a publisher by ID", manual_parameters=[id_param],
                         request_body=PublisherInputDto, responses={200: PublisherOutputDto, 400: 'Bad Request'})
    def put(self, request: Request):
        id = request.query_params.get('id')
        publisher = Publisher.objects.get(id=id)
        data = PublisherInputDto(instance=publisher, data=request.data)
        if data.is_valid():
            return Response(PublisherOutputDto(data.update(publisher, data.validated_data)).data, status=200)
        else:
            return Response(data.errors, status=400)

    @swagger_auto_schema(operation_description="Delete a publisher by ID", manual_parameters=[id_param],
                         request_body=no_body, responses={204: 'No Content', 404: 'Not found'})
    def delete(self, request: Request):
        id = request.query_params.get('id')
        publisher = Publisher.objects.get(id=id)
        publisher.delete()
        return Response(status=204)
