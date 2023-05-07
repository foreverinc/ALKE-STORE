from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Currency
from main.models import Cart



@login_required
def profile_view(request):
    cs=Currency.objects.all()
    user=request.user
    placed_orders=Cart.objects.filter(user=user,complete=True)
    if request.POST:
        email=request.POST.get('email', None)
        phone=request.POST.get('phone',None)
        currency=request.POST.get('currency', None)
        if email:
            user.email=email
            user.save()
        if phone:
            user.account.phone_number=phone
        if currency:
            currency=cs.get(id=currency)
            user.account.exchange=currency
        user.account.save()
        
        return redirect('account')
    
    context={
        'user':user,
        'cs':cs,
        'placed_orders':placed_orders,
    }
    return render(request, 'account/profile.html',context)


def currency(request):
    user=request.user.account
    if request.GET:
        currency=request.GET.get('currency')
        currency=Currency.objects.get(id=currency)
        user.exchange=currency
        user.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))

