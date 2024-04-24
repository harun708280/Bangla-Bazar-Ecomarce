from django.contrib import admin
from django.contrib import admin
from . models import *
# Register your models here.

@admin.register(customers)

class customerModelAdmin(admin.ModelAdmin):
    list_display=['id','first_name','last_name','Contract_Number','email','division','user','district','thana','Union']

@admin.register(hero)

class heroModelView(admin.ModelAdmin):
    list_display=['id','img','name']


@admin.register(Product)

class ProductModelView(admin.ModelAdmin):
    list_display=['id','name','item','price','discription','img']


@admin.register(bestsel)

class bestselModelAdmin(admin.ModelAdmin):
    list_display=['id']

@admin.register(Customer_Reivew)

class ReviewModelAdmin(admin.ModelAdmin):
    list_display=['id','name','profesion','rating','comments','img']
    
@admin.register(Cart)

class CartModelAdmin(admin.ModelAdmin):
    list_display=['id','user','product','quantity','line_total']

admin.site.register(SpacialOffer)

admin.site.register(Customer_Contract_From)
admin.site.register(onlyOne_Special_Product)
admin.site.register(OrderPlaced)
admin.site.register(Reviews)