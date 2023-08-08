from django.urls import path

from .views import ProductAPIView, ProductUpdateDeleteAPIView, AddToShoppingCardAPIView, \
    UserShoppingCardAPIView, DeleteFromCardAPIView, \
    BillingRecordsView, SendMail, SearchAPIView, \
    ProductDetailAPIView, OrderAPIView, MerchantAPIView, PutsAPIView, UsersAPIView, ClientAPIView, \
    Client_detailsAPIView, CreditAPIView, ChoosesAPIView, BuysAPIView,CreditidAPIView,ChooseidAPIView,AddToShoppingCardidAPIView,BuysidAPIView,UsersidAPIView
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='API Documentation')

urlpatterns = [
    path('api/products/', ProductAPIView.as_view(), name='products'),
    path('api/products/<int:pk>', ProductDetailAPIView.as_view(), name='products'),
    path('api/docs/', schema_view),
    path('api/add-to-card', AddToShoppingCardAPIView.as_view(), name='shopping_card'),
    path('api/user-card', UserShoppingCardAPIView.as_view(), name='user_card'),
    path('user-card-delete/<int:pk>', DeleteFromCardAPIView.as_view(), name='user_card_delete'),
    path('page/<int:pk>/', BillingRecordsView.as_view(), name='product'),
    path('user/<int:pk>/', UsersidAPIView.as_view(), name='user'),
    path('buys/<int:pk>/', BuysidAPIView.as_view(), name='product'),
    path('choose/<int:pk>/', ChooseidAPIView.as_view(), name='product'),
    path('api/cards/<int:pk>/', AddToShoppingCardidAPIView.as_view(), name='adds'),
    path('credit/<int:pk>/', CreditidAPIView.as_view(), name='product'),
    path('send-email', SendMail.as_view(), name='send_email'),
    path('search/', SearchAPIView.as_view(), name='your-model-list'),
    path('order/', OrderAPIView.as_view(), name='order'),
    path('merchant/', MerchantAPIView.as_view(), name='merchant'),
    path('merchant/<int:pk>', PutsAPIView.as_view(), name='merchant'),
    # path('users/', UsersAPIView.as_view(), name='users'),
    path('client/', ClientAPIView.as_view(), name='client'),
    path('client/<int:pk>', Client_detailsAPIView.as_view(), name='clients'),
    path('products/<int:pk>/', ProductUpdateDeleteAPIView.as_view(), name='product-update-delete'),
    path('credit/', CreditAPIView.as_view(), name='credit'),
    path('chooses/', ChoosesAPIView.as_view(), name='chooses'),
    path('buys/', BuysAPIView.as_view(), name='buys'),
]
