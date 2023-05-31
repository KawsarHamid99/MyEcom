from django.contrib import admin
from .models import Product,cart,Customer,OrderPlaced
# Register your models here.

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display=['id','title','selling_price','discounted_price','description','brand','category','product_image']

@admin.register(cart)
class AdminCart(admin.ModelAdmin):
    list_display=['id','user','product','quantity']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['id','user','name','locality','city','zipcode','state']

@admin.register(OrderPlaced)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id','user','customer','product','quantity','orderd_date','status']

