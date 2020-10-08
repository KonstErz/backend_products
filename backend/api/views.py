from django.contrib.auth import authenticate, login
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from api.models import User, Category, Company, Product
from api.serializers import (SignupSerializer, LoginSerializer,
                             CategorySerializer, CompanySerializer,
                             ProductSerializer, ProductDetailSerializer)


class SignupView(APIView):

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        phone = serializer.validated_data['phone']
        password = serializer.validated_data['password']

        user = User.objects.create_user(username=username,
                                        email=email,
                                        phone=phone,
                                        password=password)

        return Response({'User ID': user.id}, 201)


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.validated_data['username'],
                            password=serializer.validated_data['password'])

        if user is not None:
            login(request, user)
            return Response({'Token': user.auth_token.key}, 200)
        else:
            return Response({'error': 'username or password invalid'}, 400)


class CategoryList(generics.ListAPIView):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CompanyList(generics.ListAPIView):

    queryset = Company.objects.filter(is_active=True)
    serializer_class = CompanySerializer


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.filter(is_active=True).select_related(
        'category', 'company').order_by('title')
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['category', 'company']
    search_fields = ['title']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer

        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]
