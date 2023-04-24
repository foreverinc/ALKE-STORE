from django.urls import path
from .views import profile_view,currency


urlpatterns=[
    path('',profile_view,name='account'),
    path('change',currency,name='currency')
]