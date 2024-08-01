from django.contrib import admin

# Register your models here.
from .models import Product, Category,Customer,Cart
class AdminProduct(admin.ModelAdmin):
    list_display = ('id','name','price','category')
class AdminCustomer(admin.ModelAdmin):
    list_display = ('id','name','phone')
class AdminCart(admin.ModelAdmin):
    list_display=('id','phone','product','image','price')


admin.site.register(Product,AdminProduct)
admin.site.register(Category)
admin.site.register(Customer,AdminCustomer)
admin.site.register(Cart,AdminCart)
