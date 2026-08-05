from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Product, FeedingGuideline, Review, Category, Tag, ProductImage, Order, OrderItem, ShippingAddress

# Register your models here.
class FeedingGuidelineInline(admin.TabularInline):
    model = FeedingGuideline
    extra = 4
    
class ReviewInline(admin.TabularInline):
    model = Review 
    extra = 0

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'user', 'rating']

class ImagesInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    


class TagInline(admin.TabularInline):
    model = Tag 
    extra = 1
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    inlines = [TagInline, ImagesInline, FeedingGuidelineInline, ReviewInline]
    filter_horizontal = ('categories',)
    
    

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    readonly_fields = ['product', 'price', 'quantity']
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email', 'total_price', 'payment_method', 'created_at']
    inlines = [OrderItemInline]
    

class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress


admin.site.unregister(User)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines=[ShippingAddressInline]
