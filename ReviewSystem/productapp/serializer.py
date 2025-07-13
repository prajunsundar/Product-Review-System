from rest_framework import serializers
from .models import Product,Review
from django.contrib.auth.models import User


class ProductSerializer(serializers.ModelSerializer):
    average_rating=serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    class Meta:
        model=Product
        fields=['id','name','description','price','average_rating']

    def get_average_rating(self,obj):
        return obj.get_review()

    def get_price(self,obj):
        return float(obj.price)



class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    data=product=Product.objects.all()
    product=serializers.PrimaryKeyRelatedField(queryset=data,write_only=True)

    class Meta:
        model=Review
        fields=['product','username','reviews','rating']

    def validate(self, data):
        keys=['product','reviews','rating']
        if list(data.keys())!=keys:
            raise serializers.ValidationError()

        return data







class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()

    def validate(self, data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('user name already exists')
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('email already exists')

        return data

    def create(self, validated_data):
        user=User.objects.create_user(username=validated_data['username'],email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data


class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
