from django.shortcuts import render
from django.db.models import Q
from .models import *
from .serializer import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import *
from rest_framework.authentication import TokenAuthentication







class ListProduct(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        product=Product.objects.all()
        serializer=ProductSerializer(product,many=True)

        return Response(serializer.data)


class ProductDetails(APIView):
    permission_classes = [AllowAny]
    def get(self,request,product_id):
        try:
            product=Product.objects.get(id=product_id)
        except:
            return Response({'message':'product not found'},status=status.HTTP_404_NOT_FOUND)

        product_serializer = ProductSerializer(product)
        review=Review.objects.filter(product=product.id)

        if review:
            review_serializer=ReviewSerializer(review,many=True)
            context = {'products': product_serializer.data,'reviews': review_serializer.data}
            return Response(context)

        context = {'products': product_serializer.data, 'reviews':'No reviews'}
        return Response(context)




class CreateProduct(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def post(self,request):
        data=request.data
        serializer=ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'new product is added'},status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors},status=status.HTTP_400_BAD_REQUEST)




class UpdateProduct(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def put(self,request):
        data=request.data
        try:
            product = Product.objects.get(id=data['id'])
            serializer=ProductSerializer(product,data=data,partial=False)
        except:
            return Response({'message':'product not found'},status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save()
            return Response({'message':'product is updated'},status=status.HTTP_200_OK)
        return Response({'error': serializer.errors},status=status.HTTP_400_BAD_REQUEST)


    def patch(self,request):
        data=request.data
        try:
            product = Product.objects.get(id=data['id'])
            serializer=ProductSerializer(product,data=data,partial=True)
        except:
            return Response({'message':'product not found'},status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            serializer.save()
            return Response({'message':'product is updated'},status=status.HTTP_200_OK)
        return Response({'error': serializer.errors},status=status.HTTP_400_BAD_REQUEST)





class DeleteProduct(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def delete(self, request):
        data = request.data
        try:
            product = Product.objects.get(id=data['id'])
        except:
            return Response({'message': 'product not found'}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response({'message':'product is deleted'},status=status.HTTP_200_OK)





class RegisterUser(APIView):

    def post(self,request):
        data=request.data
        serializer=RegisterSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({'message':'user created'},status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors},status=status.HTTP_400_BAD_REQUEST)







class LoginUser(APIView):

    def post(self,request):
        data=request.data
        serializer=LoginSerializer(data=data)

        if serializer.is_valid():
            user=authenticate(username=serializer.data['username'],password=serializer.data['password'])
            if user:
                token,_=Token.objects.get_or_create(user=user)
                return Response({'message':'Login successfull','Token':str(token)},status=status.HTTP_200_OK)
            return Response({'error': serializer.errors},status=status.HTTP_404_NOT_FOUND)

        return Response({'error': serializer.errors},status=status.HTTP_404_NOT_FOUND)

class LogoutUser(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        request.user.auth_token.delete()
        return Response({'message': 'logout successfull'}, status=status.HTTP_200_OK)


class ReviewAdd(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        data = request.data
        if Review.objects.filter(Q(product=data['product']) & Q(user=request.user)).exists():
            return Response({'message': 'you are already reviewed this product'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReviewSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': 'Your review is added'}, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)