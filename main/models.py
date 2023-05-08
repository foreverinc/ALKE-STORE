from django.db import models
import uuid
from accounts.models import Account
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from ckeditor.fields import RichTextField
from phonenumber_field.modelfields import PhoneNumberField


class Category(models.Model):
    name = models.CharField(max_length=200)
    image_name=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.name
    
    @property
    def item_count(self):
        return Product.objects.filter(category=self).count()





class ProductImage(models.Model):
    product = models.ForeignKey('Product',on_delete=models.CASCADE,related_name='images')
    images=models.ImageField(upload_to='product_images/other/')
    
    def __str__(self):
        return self.product.name



class Product(models.Model):
    PRICE_LABELS=(
        ('A','Below $25'),
        ('B','$25 - $50'),
        ('C','Above $50')
    )
    COLORS=(
        ('RED','RED'),
        ('WHITE','WHITE'),
        ('BLACK','BLACK'),
        ('BLUE','BLUE'),
        ('GREEN','GREEN'),
        ('YELLOW','YELLOW'),
        ('MULTICOLOR','MULTICOLOR'),
        ('GRAY','GRAY'),
    )
    SIZE=(
        ('XS','XS'),
        ('S','S'),
        ('M','M'),
        ('L','L'),
        ('XL','XL'),
        ('XXL','XXL'),
    )
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=999, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    product_img = models.ImageField(upload_to='product_images/main/', null=True, verbose_name='Product picture', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    digital = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    original_price = models.DecimalField(max_digits=999, decimal_places=2, blank=True, null=True)
    description = RichTextField(verbose_name='Description')
    special_offer = models.BooleanField(default=False)
    color=MultiSelectField(choices=COLORS,max_length=100,max_choices=20,null=True,blank=True)
    size=MultiSelectField(choices=SIZE,max_length=100,max_choices=20,null=True,blank=True)
    manufacturer = models.CharField(max_length=200,null=True)
    material=models.CharField(max_length=200,blank=True,null=True)
    price_label=models.CharField(max_length=3,null=True,choices=PRICE_LABELS)
    specification = RichTextField(null=True)

    
        
        
        
    @property
    def get_url(self):
        return self.product_img.url or None
    
    @property
    def average_review(self):
        total_rating = 0
        num_reviews = 0
        for review in self.review.all():
            if review.rating:
                total_rating += review.rating
                num_reviews += 1
        if num_reviews > 0:
            return round(total_rating / num_reviews)
        else:
            return None
    @property
    def get_discount(self):
        discount = ((self.original_price - self.price) / self.original_price) * 100
        return round(discount)

    def __str__(self):
        return self.name

class Review(models.Model):
    RATING_CHOICES = (
        (1, '1 star'),
        (2, '2 stars'),
        (3, '3 stars'),
        (4, '4 stars'),
        (5, '5 stars'),
    )
    name=models.CharField(max_length=200,null=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    email=models.EmailField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='review',null=True)
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered=models.DateTimeField(auto_now_add=True)
    transaction_id=models.UUIDField(default=uuid.uuid4,primary_key=True)
    complete=models.BooleanField(default=False)
    
    
    @property
    def get_shipping(self):
        orders=self.cartitems.all()
        total=sum([item.get_total for item in orders])
        if total==0:
            shipping=0
        elif total >100:
            shipping=30
        else:
            shipping=50
        return shipping  
    
    
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
    color=models.CharField(max_length=100,null=True,blank=True)
    size=models.CharField(max_length=100,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    @property
    def get_total(self):
        total=self.product.price*self.quantity
        return total
    
    def __str__(self):
        return self.product.name
    

class ShippingAddress(models.Model):
    cart=models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    email=models.EmailField(max_length=200)
    phone=PhoneNumberField()
    street=models.CharField(max_length=200)
    other=models.CharField(max_length=200,blank=True,null=True)
    country=models.CharField(max_length=200)
    city=models.CharField(max_length=200)
    zipcode=models.CharField(max_length=200)

    def __str__(self):
        return self.first_name +'' + self.last_name

