from django.urls import path
from . import views 

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('team-details/', views.teamDetails, name='team-details'),
    path('working-process/', views.workingProcess, name='working-process'),
    path('history', views.history, name='history'),
    path('pricing', views.pricing, name='pricing'),
    path('gallery/', views.gallery, name='gallery'),
    path('sign-in/', views.signIn, name='sign-in'),
    path('services/', views.services, name='services'),
    path('service-details/', views.serviceDetails, name='service-details'),
    path('products/', views.products, name='products'),
    path('product-details/', views.productDetails, name='product-details'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('blogs/', views.blogs, name='blogs'),
    path('blog-details', views.blogDetails, name='blog-details'),
]
