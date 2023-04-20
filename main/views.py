from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Product,Cart,OrderItem,Category,Vendor,ProductImage,Review,Wishlist,Size,Color,PriceRange
from django.http import JsonResponse
import json
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
# Create your views here.


def homepage(request):
    user = request.user
    cart = None
    cartitems = None
    context = {}
    categories = Category.objects.all()
    products=Product.objects.all().order_by('-id')[:8]
    vendors=Vendor.objects.all()
    featured =  Product.objects.filter(featured=True)[:4]

    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(account=user.account, complete=False)
        cartitems = cart.cartitems.all()
        context['cart'] = cart
        context['cartitems'] = cartitems

    context['products'] = products
    context['categories'] = categories
    context['vendors']=vendors
    context['featured']=featured

    return render(request, 'base/index.html', context)




def shop(request):
    user = request.user
    cart = None
    cartitems = None
    categories = Category.objects.all()
    context={}
    colors=Color.objects.all()
    sizes=Size.objects.all()
    ranges=PriceRange.objects.all()

    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(account=user.account, complete=False)
        cartitems = cart.cartitems.all()
        context['cart'] = cart
        context['cartitems'] = cartitems
    context['colors'] = colors
    context['sizes'] = sizes
    context['ranges']= ranges
    if request.GET:
        if request.GET['category']:
            category=request.GET['category']
            products_list=Product.objects.filter(category_id=category).order_by('-id')
        elif request.GET['price_range']:
            range=request.GET['price_range']
            products_list=Product.objects.filter(price_range_id=range)
        elif request.GET['color']:
            color=request.GET['color']
            product_list=Product.objects.filter(color_id=color)
        elif request.GET['size']:
            size=request.GET['size']
            product_list=Product.objects.filter(size_id=size)
        
    else:
        products_list =Product.objects.all().order_by('-id')
    p=Paginator(products_list,9)
    page=request.GET.get('page')
    products=p.get_page(page)
    
    context['products'] = products
    context['categories'] = categories
    return render(request, 'base/shop.html',context)

@login_required
def cart_view(request):
    user=request.user
    cart, created=Cart.objects.get_or_create(account=user.account,complete=False)
    cartitems=cart.cartitems.all()
    categories = Category.objects.all()
    context={
        'items':cartitems,
        'cart':cart,
        'categories':categories
    }
    return render(request,'base/cart.html',context)

@login_required
def update_cart(request):
    user=request.user.account
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    product=Product.objects.get(id=productId)
    order,created=Cart.objects.get_or_create(account=user,complete=False)
    orderItem,created= OrderItem.objects.get_or_create(cart=order,product=product)
    if action =='add':
        orderItem.quantity=(orderItem.quantity+1)
    elif action=='remove':
        orderItem.quantity=(orderItem.quantity-1)
        
    orderItem.save()
    if orderItem.quantity<=0:
        orderItem.delete()
    
    num_items=order.get_cart_items 
    
    
    return JsonResponse(num_items,safe=False)


def update_num(request):
    if request.method == 'POST':
        item_id = request.POST.get('itemId')
        order=OrderItem.objects.get(id=item_id)
        action = request.POST.get('action')
        if action == 'remove':
            order.quantity-=1
            order.save()
        elif action == 'add':
            order.quantity+=1
            order.save()
    return redirect('cart')



def delete_order(request,id):
    item=OrderItem.objects.get(id=id)
    item.delete()
        
    return redirect('cart')




def search_view(request):
    user=request.user
    query = request.GET.get('q')
    results = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
    categories=Category.objects.all()
    status=True
    context = {'query': query, 'results': results,'status': status,'categories': categories}
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(account=user.account, complete=False)
        cartitems = cart.cartitems.all()
        context['cart'] = cart
        context['cartitems'] = cartitems
    return render(request, 'base/detail.html', context)


def subscribe(request):
    if request.POST:
        email=request.POST['email']
        print(email)
        messages.success(request, 'Thanks for subscribing')
        
    return redirect('home')


def checkout(request):
    user=request.user
    cart, created=Cart.objects.get_or_create(account=user.account,complete=False)
    cartitems=cart.cartitems.all()
    
    context={
        'items':cartitems,
        'cart':cart
    }
    
    return render(request,'base/checkout.html',context)


def contact(request):
    return render(request, 'base/contact.html')


def detail(request,pk):
    product=Product.objects.get(id=pk)
    images=ProductImage.objects.filter(product_id=pk)
    user=request.user
    
    context={
        'item':product,
        'images':images,
    }
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(account=user.account, complete=False)
        cartitems = cart.cartitems.all()
        context['cart'] = cart
        context['cartitems'] = cartitems
    return render(request,'base/detail.html',context)   

def review(request,pk):
    if request.POST:
        name=request.POST['name']
        stars=request.POST['ratings']
        email=request.POST['email']
        comment=request.POST['comment']
        product=Product.objects.get(id=pk)
        new_review=Review.objects.create(name=name,rating=stars,email=email,comment=comment,product=product)
        new_review.save()
    
    return redirect('detail',pk=pk)
         
         
@login_required
def update_wishlist(request):
    user = request.user
    data = json.loads(request.body)
    product_id = data['productId']
    product = Product.objects.get(id=product_id)
    
    try:
        wishlist = Wishlist.objects.get(user=user)
    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(user=user)
        
    if not wishlist.products.filter(id=product_id).exists():
        wishlist.products.add(product)
        wishes = wishlist.products.count()
        return JsonResponse(wishes, safe=False)
    
    wishes = wishlist.products.count()
    return JsonResponse(wishes, safe=False)

def view_wishlist(request):
    user=request.user
    wishes=Wishlist.objects.get(user=user).products.all()
    context={
        'wishes':wishes
    }
    return render(request, 'base/wishlist.html',context)