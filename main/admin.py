from django.contrib import admin
from .models import Cart, Product,Category,OrderItem,Vendor
# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(Vendor)