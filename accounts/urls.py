from django.conf.urls import url,include
from .views import *

urlpatterns = [
    url(r'^login/$', login_view, name='login'),
    url(r'logout/$', LogoutView.as_view(), name='logout'),
    url(r'signUp/$', SignUpView.as_view(), name='signup'),
    url(r'manageAccount/$', manage_account, name='manageAccount'),
    url(r'displayAddresses/', display_address, name='displayAddress'),
    url(r'deleteAddress/', AddressDelete.as_view(), name='deleteAddress'),
    url(r'addAddress/', AddressCreate.as_view(), name='addAddress'),
    url(r'updateAddress/', AddressUpdate.as_view(), name='updateAddress'),
    url(r'createcc/', CreateCreditCardView.as_view(), name='createcc'),
    url(r'displaycc/', display_cc, name='displaycc'),
    url(r'deletecc/', CreditCardDelete.as_view(), name='deletecc'),
    url(r'updatecc/', CreditCardUpdate.as_view(), name='updatecc'),
    url(r'changepw/', change_password, name='changepw')
]