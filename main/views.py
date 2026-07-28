from django.shortcuts import render
from .models import Product

# Create your views here.
def index(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'about/about.html')

def contact(request):
    return render(request, 'contact/contact.html')

def teamDetails(request):
    return render(request, 'team/team.html')

def workingProcess(request):
    return render(request, 'workingProcess/working_process.html')

def history(request):
    return render(request, 'history/history.html')

def pricing(request):
    return render(request, 'pricing/pricing.html')

def gallery(request):
    return render(request, 'gallery/gallery.html')

def signIn(request):
    return render(request, 'sign_in.html')

def services(request):
    return render(request, 'services/services.html')

def serviceDetails(request):
    return render(request, 'services/service_details.html')

def products(request):
    products = Product.objects.all()
    return render(request, 'products/products.html', {'products': products})

def productDetails(request, id):
    product = Product.objects.get(id=id)
    product_cat_names = {cat.category.lower() for cat in product.categories.all()}
    
    suggestions = []
    
    # Exclude the current product upfront
    all_products = Product.objects.exclude(id=product.id)
    
    for item in all_products:
        # Get item's category names in lowercase
        item_cat_names = {cat.category.lower() for cat in item.categories.all()}
        
        # Check if there is any string overlap
        if product_cat_names & item_cat_names:
            suggestions.append(item)
            
        if len(suggestions) == 4:
            break
        
    return render(request, 'products/product_details.html', {'product': product, 'suggestions': suggestions})

def cart(request):
    return render(request, 'ordering/cart.html')

def checkout(request):
    return render(request, 'ordering/checkout.html')

def blogs(request):
    return render(request, 'blog/blogs.html')

def blogDetails(request):
    return render(request, 'blog/blog_details.html')



