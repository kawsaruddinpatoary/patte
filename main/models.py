from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

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
    
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE) 
    
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'product')
    
    def get_total_price(self):
        return self.product.price * self.quantity
    
    def __string__(self):
        return f"{self.user.username} - {self.product.title} {self.quantity}"
    

class ShippingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="shipping_address")
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    country = models.CharField(max_length=100, default="Bangladesh")
    city = models.CharField(max_length=100, blank=True, null=True)
    division = models.CharField(max_length=100, blank=True, null=True)
    post_code = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    
    def __string__(self):
        return f"Shipping details for {self.user.username}"
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()  
    phone = models.CharField(max_length=15)
    address = models.TextField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, default="Cash On Delivery")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __string__(self):
        return f"Order #{self.id} by {self.user.username}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def get_cost(self):
        return self.price * self.quantity
    
    def __string__(self):
        return f"{self.quantity} x {self.product.title if self.product else 'Deleted Product'}. "
    
      
    
