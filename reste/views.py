from contextvars import Token
from datetime import date
from sqlite3 import IntegrityError

from coreapi.compat import force_text
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.db.models import Q, Sum
from django.utils.http import urlsafe_base64_decode
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Product, User, ShoppingCard, Order, Merchant, Users, Client, Credit, Chooses, Buys
from .serializers import ProductSerializer, ShoppingCardForDetailSerializer, ShoppingCardSerializer, \
    LargeResultsSetPagination, OrderSerializer, MerchantSerializer, UsersSerializer, ClientSerializer, \
    CreditSerializer, ChoosesSerializer, BuysSerializer, EmailSerializer
from .tasks import send_email
from rest_framework import status, generics, filters, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from .serializers import UserSerializer, LoginSerializer


class ProductAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CreditAPIView(generics.ListCreateAPIView):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer


class CreditidAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer
    lookup_url_kwarg = 'credit_id'

    def get_object(self):
        try:
            return self.queryset.get(pk=self.kwargs.get(self.lookup_url_kwarg))
        except Credit.DoesNotExist:
            raise NotFound()


class ChoosesAPIView(generics.ListCreateAPIView):
    queryset = Chooses.objects.all()
    serializer_class = ChoosesSerializer


class ChooseidAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chooses.objects.all()
    serializer_class = ChoosesSerializer


class BuysAPIView(APIView):

    def get(self, request):
        products = Buys.objects.all()
        sum_payments = Buys.calculate_sum()
        products_data = BuysSerializer(products, many=True).data
        response_data = {
            'sum_payments': sum_payments,
            'products': products_data
        }
        return Response(response_data)

    # def post(self, request):
    #     serializer = BuysSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #
    #     total_sum = sum([choose.quantity * choose.product.price for choose in Chooses.objects.all()])
    #     payment = serializer.validated_data.get('payment')
    #
    #     if total_sum > payment or payment > total_sum:
    #         send_email.delay('roncrist5575@gmail.com', f'Payment completed. No further payment required.')
    #     if payment < total_sum:
    #
    #         send_email.delay('roncrist5575@gmail.com',
    #                          f'Please make a payment. You need to pay an additional amount of {payment - total_sum}. Check our website.')
    #
    #     return Response(status=201)
    def post(self, request):
        serializer = BuysSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        buys = serializer.instance
        buys.send_email_notification()

        return Response(status=201)


class BuysidAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Buys.objects.all()
    serializer_class = BuysSerializer


class MerchantAPIView(generics.ListCreateAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer


class ClientAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class Client_detailsAPIView(APIView):
    def put(self, request, pk):
        try:
            product = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response(status=404)

        product_data = ClientSerializer(product, data=request.data)
        product_data.is_valid(raise_exception=True)
        product_data.save()

        return Response(status=200)

    def delete(self, request, pk):
        try:
            product = Client.objects.get(pk=pk)
        except Client.DoesNotExist:
            return Response(status=404)

        product.delete()
        return Response(status=204)


class UsersAPIView(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class UsersidAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer


class PutsAPIView(APIView):
    def put(self, request, pk):
        try:
            product = Merchant.objects.get(pk=pk)
        except Merchant.DoesNotExist:
            return Response(status=404)

        product_data = MerchantSerializer(product, data=request.data)
        product_data.is_valid(raise_exception=True)
        product_data.save()

        return Response(status=200)


class ProductDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product)
            return Response(serializer.data)

        except:
            return Response('This does not exist')


class ProductUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class AddToShoppingCardAPIView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = ShoppingCard.objects.all()
    serializer_class = ShoppingCardSerializer


class AddToShoppingCardidAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = ShoppingCard.objects.all()
    serializer_class = ShoppingCardSerializer


class UserShoppingCardAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user_products = ShoppingCard.objects.filter(user=request.user)
        serializer = ShoppingCardForDetailSerializer(user_products, many=True)
        summ = 0
        for element in serializer.data:
            summ += element['product']['price'] * element['quantity']
        data = {
            'data': serializer.data,
            'summ': summ
        }
        return Response(data)


class OrderAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        product_data = OrderSerializer(data=request.data)
        product_data.is_valid(raise_exception=True)
        product_data.save()
        return Response(status=201)

    def get(self, request):
        orders = Order.objects.all()
        total_price = orders.aggregate(total=Sum('price'))['total']
        serialized_orders = OrderSerializer(orders, many=True)
        response_data = {
            'orders': serialized_orders.data,
            'total_price': total_price
        }
        return Response(response_data)


class DeleteFromCardAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            ShoppingCard.objects.get(Q(pk=pk), Q(user=request.user)).delete()
        except ShoppingCard.DoesNotExist:
            return Response({'message': 'Bunday mahsulot mavjud emas'})
        return Response(status=204)


class BillingRecordsView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LargeResultsSetPagination


class SendMail(APIView):
    def post(self, request):
        try:
            serializer = EmailSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get('email')
            message = 'Test message'
            send_email.delay(email, message)
        except Exception as e:
            return Response({'success': False, 'message': f'{e}'})
        return Response({'success': True, 'message': 'Sent'})


class SearchAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'price']

    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q', None)
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) |
                Q(price__icontains=q)
            )
        return queryset
