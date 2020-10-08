from rest_framework import serializers
from api.models import User, Category, Company, Product


class SignupSerializer(serializers.Serializer):

    username = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    password = serializers.CharField()

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('username already exist')

        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('email already exist')

        return value


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'title']


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['id', 'name', 'description']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['url', 'id', 'title', 'description', 'category',
                  'company']


class ProductDetailSerializer(ProductSerializer):

    category = CategorySerializer()
    company = CompanySerializer()
