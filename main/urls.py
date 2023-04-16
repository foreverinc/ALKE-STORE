from django.urls import path
from .views import homepage,details,cart_view,update_cart,update_num,delete_order,search_view,subscribe,checkout,contact


urlpatterns=[
    path('',homepage,name='home'),
    path('get/<str:category>/',details,name='detail'),
    path('cart/',cart_view,name='cart'),
    path('update/',update_cart,name='update'),
    path('add/',update_num,name='add'),
    path('done/<int:id>',delete_order,name='done'),
    path('search/',search_view,name='search'),
    path('subscribe/',subscribe,name='subscribe'),
    path('checkout/',checkout,name='checkout'),
    path('contact/',contact,name='contact'),
]
