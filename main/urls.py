from django.urls import path
from .views import homepage,shop,cart_view,update_cart,update_num,delete_order,search_view,subscribe,checkout,contact,detail,review,about,faq,shipping,payment_confirmed,order_view,get_code


urlpatterns=[
    path('',homepage,name='home'),
    path('shop/',shop,name='shop'),
    path('cart/',cart_view,name='cart'),
    path('update/<int:pk>',update_cart,name='update'),
    path('add/',update_num,name='add'),
    path('done/<int:id>',delete_order,name='done'),
    path('search/',search_view,name='search'),
    path('subscribe/',subscribe,name='subscribe'),
    path('checkout/',checkout,name='checkout'),
    path('contact/',contact,name='contact'),
    path('detail/<int:pk>/',detail,name='detail'),
    path('review/product-<int:pk>/',review,name='review'),
    path('about/',about,name='about'),
    path('faq/',faq,name="faq"),
    path('shipping/',shipping,name='shipping'),
    path('payment_confirmed/',payment_confirmed,name='payment_confirmed'),
    path('order/<uuid:pk>/',order_view,name='order'),
    path('get/',get_code,name='get')
]
