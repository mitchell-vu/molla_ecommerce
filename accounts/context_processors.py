from .models import Wishlist


def wishlist(request):
    if 'admin' in request.path:
        return {}
    else:
        current_user = request.user
        wishlist_counter = 0
        
        if current_user.is_authenticated:
          wishlist_counter = Wishlist.objects.filter(user=current_user).count
        
    return dict(
        wishlist_counter=wishlist_counter,
    )
