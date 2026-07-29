from django.shortcuts import render
from django.core.paginator import Paginator
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
    product_list = Product.objects.all().order_by('-id')
    
    # 1. Show 8 products per page (change this number as needed)
    paginator = Paginator(product_list, 8) 
    
    # 2. Get current page number from URL query string (e.g. ?page=2)
    page_number = request.GET.get('page')
    
    # 3. Get products for that specific page
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,  # This replaces your old 'products' variable
    }
    return render(request, 'products/products.html', context)

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



