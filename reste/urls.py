from django.urls import path

from accounts.views import UserRegistrationAPIView, UserLoginAPIView
from .views import ProductAPIView, ProductUpdateDeleteAPIView, AddToShoppingCardAPIView, \
    UserShoppingCardAPIView, DeleteFromCardAPIView, \
    BillingRecordsView, SendMail, SearchAPIView, \
    ProductDetailAPIView, CardlistAPIView,OrderAPIView,MerchantAPIView,PutsAPIView,UsersAPIView,ClientAPIView,Client_detailsAPIView
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API Documentation')

urlpatterns = [
    path('products/', ProductAPIView.as_view(), name='products'),
    path('product-update-delete/<int:pk>', ProductUpdateDeleteAPIView.as_view(), name='products_update_delete'),
    path('products/<int:pk>', ProductDetailAPIView.as_view(), name='products'),
    path('docs/', schema_view),
    path('card_list/', CardlistAPIView.as_view(), name='card_list'),
    path('add-to-card', AddToShoppingCardAPIView.as_view(), name='shopping_card'),
    path('user-card', UserShoppingCardAPIView.as_view(), name='user_card'),
    path('user-card-delete/<int:pk>', DeleteFromCardAPIView.as_view(), name='user_card_delete'),
    path('page/<int:pk>/', BillingRecordsView.as_view(), name='product'),
    path('send-email', SendMail.as_view(), name='send_email'),
    path('search/', SearchAPIView.as_view(), name='your-model-list'),
    path('register/', UserRegistrationAPIView.as_view(), name='register'),
    path('login/', UserLoginAPIView.as_view(), name='logout'),
    path('order/', OrderAPIView.as_view(), name='order'),
    path('merchant/', MerchantAPIView.as_view(), name='merchant'),
    path('merchant/<int:pk>', PutsAPIView.as_view(), name='merchant'),
    path('users/', UsersAPIView.as_view(), name='users'),
    path('client/', ClientAPIView.as_view(), name='client'),
    path('client/<int:pk>', Client_detailsAPIView.as_view(), name='clients'),
]
