from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, OrderItem, Category, ProductImage, Review,ShippingAddress
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
# Create your views here.


def homepage(request):
    context = {}
    products = Product.objects.select_related('category').prefetch_related('review').all().order_by("-id")[:4]
    
    categories = Category.objects.all()
    context["products"] = products
    
    context['categories'] = categories
    return render(request, "base/index.html", context)




def shop(request):

    context = {}

    products_list = Product.objects.select_related('category').prefetch_related('review').all().order_by("id")

    try:
        if "price" in request.GET:
            price = request.GET["price"]
            products_list = Product.objects.filter(price_label=price).order_by("id")
        elif "category" in request.GET:
            category = request.GET["category"]
            products_list = Product.objects.filter(category_id=category).order_by("id")
        elif "q" in request.GET:
            q = request.GET["q"]
            products_list = Product.objects.filter(
                Q(name__icontains=q) | Q(description__icontains=q)
            ).order_by("id")
    except:
        pass

    if request.method == "POST":
        min_price = request.POST.get("min")
        max_price = request.POST.get("max")
        if min_price and max_price:
            products_list = products_list.filter(
                price__gte=min_price, price__lte=max_price
            )

    p = Paginator(products_list, 9)
    page = request.GET.get("page")
    products = p.get_page(page)

    context["products"] = products
    return render(request, "base/shop.html", context)


@login_required
def cart_view(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user, complete=False)
    cartitems = cart.cartitems.all()

    context = {"items": cartitems, "cart": cart}
    return render(request, "base/cart.html", context)


@login_required
def update_cart(request, pk):
    if request.method == "POST":
        quantity = request.POST.get("quantity")
        color = request.POST.get("color", None)
        size = request.POST.get("size", None)
        user = request.user
        product = Product.objects.get(pk=pk)
        cart = Cart.objects.filter(user=user, complete=False).first()  # get the first cart that matches the conditions
        if cart is None:
            cart = Cart.objects.create(user=user)
        order, created = OrderItem.objects.get_or_create(product=product, cart=cart, color=color, size=size, quantity=quantity)
        if not created:
            order.quantity = quantity
            order.save()
        messages.success(request, "Item successfully added to cart")
    return redirect("cart")


@login_required
def update_num(request):
    if request.method == "POST":
        item_id = request.POST.get("itemId")
        order = OrderItem.objects.get(id=item_id)
        action = request.POST.get("action")
        if action == "remove":
            if order.quantity <= 0:
                order.delete()
            else:
                order.quantity -= 1
                order.save()
        elif action == "add":
            order.quantity += 1
            order.save()
    return redirect("cart")

@login_required
def delete_order(request, id):
    item = OrderItem.objects.get(id=id)
    item.delete()

    return redirect("cart")


def search_view(request):
    query = request.GET.get("q")
    results = Product.objects.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
    categories = Category.objects.all()
    status = True
    context = {
        "query": query,
        "results": results,
        "status": status,
        "categories": categories,
    }

    return render(request, "base/detail.html", context)


def subscribe(request):
    if request.POST:
        email = request.POST["email"]
        messages.success(request, "Thanks for subscribing")

    return redirect("home")

@login_required
def checkout(request):
    user = request.user
    cart, created = Cart.objects.get_or_create(user=user, complete=False)
    cartitems = cart.cartitems.all()

    context = {"items": cartitems, "cart": cart}

    return render(request, "base/checkout.html", context)


def contact(request):
    return render(request, "base/contact.html")


def detail(request, pk):
    product = Product.objects.get(id=pk)
    images = ProductImage.objects.filter(product_id=pk)
    others=Product.objects.filter(category=product.category).exclude(id=pk)
    context = {
        "item": product,
        "images": images,
        "others":others
    }

    return render(request, "base/detail.html", context)


@login_required
def review(request, pk):
    user = request.user
    if request.POST:
        name = request.POST["name"]
        stars = request.POST["ratings"]
        email = request.POST["email"]
        comment = request.POST["comment"]
        product = Product.objects.get(id=pk)
        new_review = Review.objects.create(
            name=name,
            rating=stars,
            email=email,
            comment=comment,
            product=product,
            user=user,
        )
        new_review.save()

    return redirect("detail", pk=pk)


def about(request):
    return render(request, "base/about.html")


def faq(request):
    return render(request, "base/faq.html")


def shipping(request):
    if request.method == 'POST':
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        email = request.POST.get('email')
        mobile_number = request.POST.get('phone')
        street_address = request.POST.get('street')
        country = request.POST.get('country')
        city = request.POST.get('city')
        apartment = request.POST.get('other')
        zip_code = request.POST.get('zip')
        cart_id = request.POST.get('cart')
        cart = Cart.objects.get(transaction_id=cart_id)
        # Check if there is already a shipping address for the current cart
        try:
            shipping = ShippingAddress.objects.get(cart=cart)
            # Update the existing shipping address
            shipping.first_name = first_name
            shipping.last_name = last_name
            shipping.email = email
            shipping.phone = mobile_number
            shipping.street = street_address
            shipping.other = apartment
            shipping.country = country
            shipping.city = city
            shipping.zipcode = zip_code
            shipping.save()
        except ShippingAddress.DoesNotExist:
            # Create a new shipping address
            
            shipping = ShippingAddress.objects.create(first_name=first_name, last_name=last_name,email=email,phone=mobile_number,street=street_address,other=apartment,country=country,zipcode=zip_code,city=city,cart=cart)
        
        # Return a success message or redirect to a success page
        return redirect('home')



def payment_confirmed(request):
    # Get the form data from the POST request
    cart_id = request.POST['cart']
    cart = Cart.objects.get(transaction_id=cart_id)
    cart.complete=True
    cart.save()
    return redirect('shop')


def order_view(request,pk):
    cart= Cart.objects.get(transaction_id=pk)
    cartitems = cart.cartitems.all()

    context = {"items": cartitems, "cart": cart}
    return render(request,'base/order.html',context)