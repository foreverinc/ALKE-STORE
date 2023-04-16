from django.db import models
import uuid
from accounts.models import Account
from django.contrib.auth.models import User
from django.db.models import Count

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    @property
    def item_count(self):
        return Product.objects.filter(category=self).count()


class Product(models.Model):
    name=models.CharField(max_length=200)
    price=models.DecimalField(max_digits=10000,decimal_places=2)
    category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
    product_img=models.ImageField(upload_to='product_images',null=True,verbose_name='Product picture',blank=True)
    files=models.FileField(upload_to='product_images',null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    digital=models.BooleanField(default=False)
    featured=models.BooleanField(default=False)
    original_price=models.DecimalField(max_digits=10000,decimal_places=2,blank=True,null=True)
    description=models.CharField(blank=True,null=True,verbose_name='Description',max_length=200)
    rating=models.PositiveIntegerField(default=0)
    rated_by=models.ManyToManyField(User,blank=True)
    special_offer=models.BooleanField(default=False)
    
    @property
    def get_rating(self):
        return self.rated_by.all().count()
    
    def __str__(self):
        return self.name

class Cart(models.Model):
    account=models.ForeignKey(Account,on_delete=models.CASCADE)  
    date_ordered=models.DateTimeField(auto_now_add=True)
    transaction_id=models.UUIDField(default=uuid.uuid4,primary_key=True)
    complete=models.BooleanField(default=False)  
    
    
    @property
    def get_cart_total(self):
        orders=self.cartitems.all()
        total=sum([item.get_total for item in orders])
        return total
    
    @property
    def get_cart_items(self):
        orders=self.cartitems.all()
        total=sum([item.quantity for item in orders])
        return total
    
    
    def __str__(self):
        return str(self.transaction_id)

class OrderItem(models.Model):
    product=models.ForeignKey(Product, related_name='items',on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,blank=True,null=True,related_name='cartitems')
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total=self.product.price*self.quantity
        return total
    
    def __str__(self):
        return self.product.name
    
class Vendor(models.Model):
    name=models.CharField(max_length=200)
    img=models.ImageField(upload_to='vendors/')
    
    def __str__(self):
        return self.name