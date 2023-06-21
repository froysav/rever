from django.contrib import admin

from reste.models import Product, ShoppingCard,Merchant,Order

admin.site.register(Product)
admin.site.register(ShoppingCard)
admin.site.register(Merchant)
admin.site.register(Order)