from django.contrib import admin
from .models import Cart, Product,Category,OrderItem,ProductImage,Review,BillingAddress,ShippingAddress
# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(ProductImage)
admin.site.register(Review),
admin.site.register(BillingAddress)
admin.site.register(ShippingAddress)
