from django.conf.urls import url,include
from .views import *


urlpatterns = [
    url(r'^login/$', login_view, name='login'),
    url(r'logout/$', LogoutView.as_view(), name='logout'),
    url(r'signUp/$', SignUpView.as_view(), name='signup'),
    url(r'changePassword/$', change_password, name='changePassword'),
    url(r'manageAccount/$', manage_account, name='manageAccount'),
    url(r'displayAddresses/', display_address, name='displayAddress'),
    url(r'deleteAddress/', AddressDelete.as_view(), name='deleteAddress'),
    url(r'addAddress/', AddressCreate.as_view(), name='addAddress'),
    url(r'updateAddress/', update_address, name='updateAddress'),
    url(r'managecc/', EditCreditCardView.as_view(), name='managecc')
]