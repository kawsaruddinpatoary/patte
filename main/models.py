from django.db import models
from django.utils.text import slugify

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    stocks = models.IntegerField()
    vitamin_e = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    glucosamine = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    crude_protein = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    moisture = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return self.title
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    body = models.TextField()
    posted_at = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}'s {self.rating}-star review for {self.product.title}"

class FeedingGuideline(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='feeding_guidelines')
    weight = models.IntegerField()
    cups = models.IntegerField()
    mix_with = models.CharField(max_length=100)
    
class Category(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='categories')
    category = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, blank=True)  # New Slug Field

    def save(self, *args, **kwargs):
        if not self.slug and self.category:
            self.slug = slugify(self.category)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category
    
class Tag(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name='tags')
    tag = models.CharField(max_length=50)
    
    
