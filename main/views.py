from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .models import Product,Cart,OrderItem,Category,Vendor
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
    

    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(account=user.account, complete=False)
        cartitems = cart.cartitems.all()
        context['cart'] = cart
        context['cartitems'] = cartitems

    context['products'] = products
    context['categories'] = categories
    context['vendors']=vendors

    return render(request, 'base/index.html', context)


def details(request, category):
    user=request.user
    status=False
    items_list = Product.objects.filter(category_id=category).order_by('-date_added')
    category=Category.objects.get(id=category).name
    p=Paginator(items_list,3)
    page=request.GET.get('page')
    items=p.get_page(page)
    categories=Category.objects.all()
    context = {
        'items': items,
        'category':category,
        'categories': categories,
        'status': status
    }
    if user.is_authenticated:
        cart, created = Cart.objects.get_or_create(account=user.account, complete=False)
        cartitems = cart.cartitems.all()
        context['cart'] = cart
        context['cartitems'] = cartitems
    return render(request, 'base/detail.html', context=context)



@login_required
def cart_view(request):
    user=request.user
    cart, created=Cart.objects.get_or_create(account=user.account,complete=False)
    cartitems=cart.cartitems.all()
    
    context={
        'items':cartitems,
        'cart':cart
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
        