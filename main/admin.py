from django.contrib import admin
from .models import Product, FeedingGuideline, Review, Category, Tag, ProductImage

# Register your models here.
class FeedingGuidelineInline(admin.TabularInline):
    model = FeedingGuideline
    extra = 4
    
class ReviewInline(admin.TabularInline):
    model = Review 
    extra = 2

class ImagesInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    
class CategoryInline(admin.TabularInline):
    model = Category 
    extra = 3

class TagInline(admin.TabularInline):
    model = Tag 
    extra = 5
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    inlines = [CategoryInline, TagInline, ImagesInline, FeedingGuidelineInline, ReviewInline]
    

