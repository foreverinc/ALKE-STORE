from django import template

register = template.Library()



# register=template.Library()
# @register.inclusion_tag('base/wishes.html',takes_context=True)
# def count_wishes(context):
#     request_user=context['request'].user
#     wishlist = Wishlist.objects.get(user=request_user).products.count()
#     return{'wishes':wishlist}