from amqp import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer, EmailField
from .models import Product, User, ShoppingCard, Order
from rest_framework import serializers, pagination
from django.utils import timezone
from reste.tasks import send_email

from amqp import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer, EmailField
from .models import Product, User, ShoppingCard, Merchant, Users, Client, Credit, Chooses, Buys
from rest_framework import serializers, pagination


class ProductSerializer(ModelSerializer):
    # category = CategorySerializer()
    # color = ColorSerializer

    after_sale = serializers.SerializerMethodField()

    def get_after_sale(self, obj):
        price = obj.price
        sale = obj.sale

        if sale is not None and sale > 0:
            after_sale = price - (price * (sale / 100))
        else:
            after_sale = price

        return after_sale

    class Meta:
        model = Product
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = '__all__'


class ChoosesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chooses
        fields = '__all__'


class BuysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buys
        fields = '__all__'

    def create(self, validated_data):
        validated_data['date'] = timezone.now()
        buys = super().create(validated_data)

        send_email.delay('roncrist5575@gmail.com',
                         f'Please do payment you should do payment {buys.date}. Check our website.')

        return buys



class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)


class ProductSerializerForCard(ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'price', 'category')


class MerchantSerializer(ModelSerializer):
    class Meta:
        model = Merchant
        fields = '__all__'


class ShoppingCardSerializer(ModelSerializer):
    class Meta:
        model = ShoppingCard
        fields = ('product', 'quantity', 'user', 'date')


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ProducteSerializer(Serializer):
    email = EmailField()

    def get_after_sale(self, obj):
        price = obj.price
        sale = obj.sale

        if sale is not None and sale > 0:
            after_sale = price - (price * (sale / 100))
        else:
            after_sale = price

        return after_sale

    class Meta:
        model = Product
        fields = '__all__'


class ShoppingCardForDetailSerializer(ModelSerializer):
    product = ProductSerializerForCard()

    class Meta:
        model = ShoppingCard
        fields = ('product', 'quantity')


class LargeResultsSetPagination(PageNumberPagination):
    def paginate_queryset(self, queryset, request, view=None):
        pk = view.kwargs.get('pk')
        if not queryset.filter(pk=pk).exists():
            raise NotFound("Object not found with this pk")

        return super().paginate_queryset(queryset, request, view)


class EmailSerializer(Serializer):
    email = EmailField()
