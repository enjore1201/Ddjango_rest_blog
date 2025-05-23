from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import SignUpSerializer, UsernameSerializer


# Create your views here.

class SignUpAPIView(CreateAPIView):
    serializer_class = SignUpSerializer

    @swagger_auto_schema(request_body=SignUpSerializer, responses={200: UsernameSerializer(many=False)})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # refresh = RefreshToken.for_user(serializer.instance)
        #
        # reponse_data = {
        #     'refresh': str(refresh),
        #     'access': str(refresh.access_token),
        # }

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
