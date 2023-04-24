from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from .models import Currency

# Create your views here.

@login_required
def profile_view(request):
    user=request.user
    account=user.account
    context={
        'user':user,
        'account':account
    }
    return render(request, 'account/profile.html')

def currency(request):
    user=request.user.account
    if request.GET:
        currency=request.GET.get('currency')
        currency=Currency.objects.get(id=currency)
        user.exchange=currency
        user.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))