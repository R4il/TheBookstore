from django.conf.urls import url, include
from .views import *

urlpatterns = [

    # /cart/id/
    url(r'^(?P<book_id>[0-9]+)/$', cart, name='cart'),
    
    # /cart/checkout/
    url(r'checkout/', checkout, name='checkout'),
    
    # /cart/
    url(r'', displayCart, name='displayCart'),
    
]
