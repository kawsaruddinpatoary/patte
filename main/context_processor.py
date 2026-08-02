from .models import CartItem, WishlistItem

def user_data(request):
    context = {
        'cart_items': [],
        'favourites': [],
        'cart_count': 0,
        'favourite_count': 0,
        'cart_total': 0,
    }
    
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user).select_related("product")
        favourites = WishlistItem.objects.filter(user=request.user).select_related("product")
        
        context["cart_items"] = cart_items
        context["favourites"] = favourites
        context["cart_count"] = sum(item.quantity for item in cart_items)
        context["favourite_count"] = len(favourites)
        context["cart_total"] = sum(item.get_total_price() for item in cart_items)
    
    
    return context