from django.db import models
from django.db import models
from flask import request
from django.contrib.auth.models import User


class Merchant(models.Model):
    type_merchant = models.CharField(max_length=100)
    name_shop = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    addres = models.TextField()
    name_bank = models.CharField(max_length=100)
    mfo = models.IntegerField()
    bank_number = models.IntegerField()

    def __str__(self):
        return self.type_merchant


class Product(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    image = models.ImageField()
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    firm = models.CharField(max_length=100)
    model_product = models.CharField(max_length=100)
    ikpu_product = models.CharField(max_length=100)
    color_product = models.CharField(max_length=100)
    country_manufacture = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name


class ShoppingCard(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Shopping Card'
        verbose_name_plural = 'Shopping Cards'

    def __str__(self):
        return self.product.name


class Order(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    rassrochka = models.DateTimeField(auto_now_add=True)
    every_pays = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    own_partifition = models.IntegerField()
    installment_balance = models.IntegerField()
    status = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    number_cart = models.IntegerField()
    valid_about = models.IntegerField()

    def __str__(self):
        return self.name


class Users(models.Model):
    phone_number = models.IntegerField()
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.TextField()

    def __str__(self):
        return self.name


class Client(models.Model):
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    pnfl = models.IntegerField()
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    passport_number = models.IntegerField()
    issued = models.CharField(max_length=100)
    date_give = models.DateTimeField(auto_now_add=True)
    goden_about = models.DateTimeField(auto_now_add=True)
    nationality = models.CharField(max_length=100)
    citizienship = models.CharField(max_length=100)
    whos_addres = models.CharField(max_length=100)
    whos_number = models.CharField(max_length=100)
    number_card = models.IntegerField()
    term_card = models.IntegerField()

    def __str__(self):
        return self.name
