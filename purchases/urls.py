from django.conf.urls import url, include
from .views import *

urlpatterns = [

    # /cart/id/
    url(r'^(?P<book_id>[0-9]+)/$', cart, name='cart'),
    
    # /cart/checkout/
    url(r'checkout/', checkout, name='checkout'),
    
    # /cart/wishlist/id/
    url(r'wishlist/drop/(?P<book_id>[0-9]+)/', dropWishlist, name='dropWishlist'),
    
    # /cart/checkout/
    url(r'wishlist/', displayWishlist, name='displayWishlist'),
    
    # /cart/checkout/
    url(r'drop/(?P<book_id>[0-9]+)/', drop, name='drop'),
    
    
    # /cart/
    url(r'', displayCart, name='displayCart'),
    
]
