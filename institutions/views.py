from django.contrib.auth.hashers import check_password, make_password
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .permissions import CertificatePermissions, InstitutionPermissions, UserPermissions
from users.models import User
from users.serializers import LoginSerializer, RegisterSerializer
from .models import Institution, Certificate
from .serializers import InstitutionSerializer, CertificateSerializer
from django.shortcuts import get_object_or_404


class RegisterAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, UserPermissions]

    @extend_schema(
        summary="User Registration",
        description="Register a new user",
        request=RegisterSerializer,  # Correctly specify the request body
        responses={
            201: OpenApiResponse(response=RegisterSerializer, description="JWT access token and refresh token"),
            400: OpenApiResponse(description="Invalid input data")
        },
        tags=["User Authentication API"]
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User has been created"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @extend_schema(
        summary="User Login",
        description="Login user with email and password",
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(response=LoginSerializer, description="JWT access token and refresh token"),
            400: OpenApiResponse(description="Invalid credentials")
        },
        tags=["User Authentication API"]
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user_obj = User.objects.get(email=user)
            except User.DoesNotExist: # noqa
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            if user_obj and check_password(password, user_obj.password):
                refresh = RefreshToken.for_user(user_obj)
                access_token = str(refresh.access_token)

                return Response(
                    {
                        "refresh": str(refresh),
                        "access": access_token
                    }, status=status.HTTP_200_OK
                )

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class InstitutionReadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, InstitutionPermissions]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @extend_schema(
        summary="Institutions Read",
        description="Institutions Read API Views",
        tags=["Institutions API"],
        responses={200: InstitutionSerializer}
    )
    def get(self, request):
        institutions = Institution.objects.all() # noqa
        serializer = InstitutionSerializer(institutions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InstitutionCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, InstitutionPermissions]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @extend_schema(
        summary="Institutions Create API",
        description="Create institutions with required fields",
        request=InstitutionSerializer,
        responses={
            200: OpenApiResponse(response=InstitutionSerializer, description="Institutions has been created"),
            400: OpenApiResponse(description="Invalid credentials")
        },
        tags=["Institutions API"]
    )
    def post(self, request):
        serializer = InstitutionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(admin=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificateReadAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CertificatePermissions]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @extend_schema(
        summary="Certificate Read API",
        description="Certificate Read API Views",
        tags=["Certificate API"],
        responses={200: CertificateSerializer}
    )
    def get(self, request):
        certificates = Certificate.objects.all() # noqa
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CertificateCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CertificatePermissions]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @extend_schema(
        summary="Certificate Create API",
        description="Create certificate with required field",
        request=CertificateSerializer,
        responses={
            200: OpenApiResponse(response=CertificateSerializer, description="Certificate has been created"),
            400: OpenApiResponse(description="Invalid credentials")
        },
        tags=["Certificate API"]
    )
    def post(self, request):
        serializer = CertificateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CertificateDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny, CertificatePermissions]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    @extend_schema(
        summary="Certificate Details API",
        description="Detail information about Certificate",
        tags=["Certificate API"],
        responses={200: CertificateSerializer}
    )
    def get(self, request, pk):
        certificate = get_object_or_404(Certificate, pk=pk)
        serializer = CertificateSerializer(certificate)
        return Response(serializer.data, status=status.HTTP_200_OK)
