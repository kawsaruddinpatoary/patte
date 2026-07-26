from django.shortcuts import render

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
    return render(request, 'products/products.html')

def productDetails(request):
    return render(request, 'products/product_details.html')

def cart(request):
    return render(request, 'ordering/cart.html')

def checkout(request):
    return render(request, 'ordering/checkout.html')

def blogs(request):
    return render(request, 'blog/blogs.html')

def blogDetails(request):
    return render(request, 'blog/blog_details.html')



