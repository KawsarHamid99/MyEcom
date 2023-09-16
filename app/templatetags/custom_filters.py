from django import template

from app.models import Category,cart

register = template.Library()

@register.simple_tag
def my_custom_tag():
    # Your custom tag logic here
    fashion=Category.objects.filter(parent=7)
    health_beauty=Category.objects.filter(parent=5)
    gift=Category.objects.filter(parent=6)
    electronics=Category.objects.filter(parent=4)

    categorylist={"fashion":fashion,"health_beauty":health_beauty,"gift":gift,"electronics":electronics}
    return categorylist

@register.simple_tag
def cart_filter(value):
    cartcount=cart.objects.filter(user=value).exists()
    if cartcount:
        cartcount=cart.objects.filter(user=value).count()
    return cartcount

