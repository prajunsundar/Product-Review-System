from django.urls import path
from .views import *

urlpatterns=[
    path('list/',ListProduct.as_view(),name='list-product'),
    path('details/<int:product_id>/',ProductDetails.as_view(),name='product-details'),

    path('create/', CreateProduct.as_view(), name='create-product'),
    path('update/', UpdateProduct.as_view(), name='update-product'),
    path('delete/', DeleteProduct.as_view(), name='delete-product'),

    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),

    path('review/', ReviewAdd.as_view(), name='review'),

]