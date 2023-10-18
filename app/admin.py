from django.contrib import admin
from .models import Product,cart,Customer,OrderPlaced,Brand
# Register your models here.

@admin.register(Product)
class AdminProduct(admin.ModelAdmin):
    list_display=['id','title','selling_price','discounted_price','description','brand','category','key_word','product_image']

@admin.register(cart)
class AdminCart(admin.ModelAdmin):
    list_display=['id','user','product','quantity']

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display=['id','user','name','address','city','zipcode','state']

@admin.register(OrderPlaced)
class OrderAdmin(admin.ModelAdmin):
    list_display=['id',"orderid",'trcking_id','user','customer','product','quantity','price_per_unit','address','orderd_date','status']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display=['id','name','image','Category_list']

from .models import Category
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin

class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title',)
    list_display_links = ('indented_title',)
    search_fields = ('name',)

    def indented_title(self, obj):
        return mark_safe(
            '&nbsp;&nbsp;&nbsp;' * (obj.level - 1) + str(obj)
        )

    indented_title.short_description = 'Category'

admin.site.register(Category, CategoryAdmin)
