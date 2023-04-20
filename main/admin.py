from django.contrib import admin
from .models import Cart, Product,Category,OrderItem,Vendor,ProductImage,Review,Wishlist,PriceRange,Size,Color,Promotion
# Register your models here.
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Category)
admin.site.register(OrderItem)
admin.site.register(Vendor)
admin.site.register(ProductImage)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(Color)
admin.site.register(PriceRange)
admin.site.register(Size)
admin.site.register(Promotion)