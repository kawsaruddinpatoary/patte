from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Count, Min
from django.db.models.functions import Lower
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product, Category, CartItem, WishlistItem
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    featured_products = Product.objects.all().order_by('-id')[:4]
    return render(request, 'home/index.html', {"featured_products": featured_products})

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
    product_list = Product.objects.all().order_by('id')
    
    categories = Category.objects.annotate(
        cat_name = Lower('category')
    ).values('cat_name').annotate(
        product_count = Count('product', distinct=True),
        slug = Min('slug')
    ).order_by('cat_name')
    
    # 1. Show 8 products per page (change this number as needed)
    paginator = Paginator(product_list, 8) 
    
    # 2. Get current page number from URL query string (e.g. ?page=2)
    page_number = request.GET.get('page')
    
    # 3. Get products for that specific page
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,  # This replaces your old 'products' variable
        'categories':categories
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


def categoryDetails(request, slug):
    product_list = Product.objects.filter(
        categories__slug__iexact = slug
    ).distinct()
    
    categories = Category.objects.annotate(
        cat_name = Lower('category')
    ).values('cat_name').annotate(
        product_count = Count('product', distinct=True),
        slug = Min('slug')
    ).order_by('cat_name')
    
    # 1. Show 8 products per page (change this number as needed)
    paginator = Paginator(product_list, 8) 
    
    # 2. Get current page number from URL query string (e.g. ?page=2)
    page_number = request.GET.get('page')
    
    # 3. Get products for that specific page
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,  # This replaces your old 'products' variable
        'categories':categories
    }
    return render(request, 'products/categoryProducts.html', context)


def auth(request):      
    loginform = LoginForm()
    registerform = RegisterForm()
    
    if request.method == "POST":
        action_type = request.POST.get('action_type')
        if action_type == "register":
            registerform = RegisterForm(request.POST)
            if registerform.is_valid():
                full_name = registerform.cleaned_data["full_name"]
                identifier = registerform.cleaned_data["username_or_email"]
                password = registerform.cleaned_data["password"]
                
                if '@' in identifier:
                    email = identifier
                    username = identifier.split('@')[0]
                else:
                    email = ''
                    username = identifier
                
                full_name_str = str(registerform.cleaned_data['full_name']).strip()

                # 2. Split by spaces into a list of word strings
                name_words = full_name_str.split()  # .split() with no arguments splits by any whitespace!

                if name_words:
                    first_name = name_words[0]  # First word
                    last_name = " ".join(name_words[1:]) if len(name_words) > 1 else ''  # Rest of the words joined together
                else:
                    first_name = ''
                    last_name = ''
                
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                login(request, user)
                messages.success(request, "Account created successfully!")
                
                return redirect('home')
            else:
                print(registerform.errors)
        
        if action_type=='login':
            loginform = LoginForm(request.POST)
            if loginform.is_valid():
                identifier = loginform.cleaned_data["username_or_email"]
                password = loginform.cleaned_data["password"]
                remember_me = loginform.cleaned_data["remember_me"]
            
                user_obj = User.objects.filter(email__iexact=identifier).first()
                username_to_auth = user_obj.username if user_obj else identifier
                
                user = authenticate(request, username=username_to_auth, password=password)
                
                if user is not None:
                    login(request, user)
                
                    if not remember_me:
                        request.session.set_expiry(0)
                    else:
                        request.session.set_expiry(1209600) # 2 weeks
                    
                    messages.success(request, f"Welcome Back {user.first_name or user.username}!")
                    return redirect('home')
                else:
                    messages.error(request, "Invalid username/Password!")
    
    context = {
        'login_form': loginform,
        'register_form': registerform,
    }
    return render(request, 'sign_in.html', context)

@login_required(login_url='sign-in')
def addToCart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Quantity for the product is increased successfully!")
    else:
        messages.success(request, "Added this product to your cart successfully!")
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))
                
                
   
   
@login_required(login_url='sign-in')
def toggleFavourite(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        wishlist_item.delete()
        messages.info(request, f"Item removed from your favourites!")
    else:
        messages.success(request, "Added this product to your favourites successfully!")
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))       


@login_required(login_url='sign-in')
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.get_total_price() for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'ordering/cart.html', context)      