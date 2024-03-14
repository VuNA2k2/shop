from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from elasticsearch_dsl import Q

from book.dto.book.book_output_dto import BookOutputDto
from clothe.dto.clothe.clothe_output_dto import ClotheOutputDto
from mobile.dto.mobile_output_dto import MobileOutputDto
from search.documents import BookDocument, MobileDocument, ClotheDocument


class BookSearchController(APIView):
    query_param = openapi.Parameter('query', in_=openapi.IN_QUERY, description='Search term', type=openapi.TYPE_STRING)

    def generate_q_expression(self, search_term):
        return Q("multi_match", query=search_term,
                 fields=["title", "description", "year", "language", "author.name", "author.email", "author.phone",
                         "publishers.name", "publishers.email", "publishers.phone", "category.name",
                         "category.description"], fuzziness="AUTO")

    @swagger_auto_schema(operation_description="Search for books", manual_parameters=[query_param],
                         responses={200: BookOutputDto(many=True)})
    def get(self, request):
        query = request.query_params.get("query", "")
        q = self.generate_q_expression(query)
        response = BookDocument.search().query(q).execute()
        response_list = [hit.to_dict() for hit in response]
        return Response(response_list)


class MobileSearchController(APIView):
    query_param = openapi.Parameter('query', in_=openapi.IN_QUERY, description='Search term', type=openapi.TYPE_STRING)

    def generate_q_expression(self, search_term):
        return Q("multi_match", query=search_term,
                 fields=['name', 'description', 'brand', 'model', "category.name",
                         "category.description"], fuzziness="AUTO")

    @swagger_auto_schema(operation_description="Search for mobiles", manual_parameters=[query_param],
                         responses={200: MobileOutputDto(many=True)})
    def get(self, request):
        query = request.query_params.get("query", "")
        q = self.generate_q_expression(query)
        response = MobileDocument.search().query(q).execute()
        response_list = [hit.to_dict() for hit in response]
        return Response(response_list)


class ClotheSearchController(APIView):
    query_param = openapi.Parameter('query', in_=openapi.IN_QUERY, description='Search term', type=openapi.TYPE_STRING)

    def generate_q_expression(self, search_term):
        return Q("multi_match", query=search_term,
                 fields=['name', 'description', 'brand', 'model', "category.name",
                         "category.description"], fuzziness="AUTO")

    @swagger_auto_schema(operation_description="Search for clothes", manual_parameters=[query_param],
                         responses={200: ClotheOutputDto(many=True)})
    def get(self, request):
        query = request.query_params.get("query", "")
        q = self.generate_q_expression(query)
        response = ClotheDocument.search().query(q).execute()
        response_list = [hit.to_dict() for hit in response]
        return Response(response_list)
