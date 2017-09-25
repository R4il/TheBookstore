from django.conf.urls import url,include
from . import views


urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'logout/$',views.LogoutView.as_view(), name='logout'),
    url(r'signUp/$',views.SignUpView.as_view(), name='signup'),
    url(r'changePassword/$',views.change_password, name='changePassword'),
    url(r'manageAccount/$', views.manage_account, name='manageAccount'),
    url(r'displayAddresses/', views.display_address, name='displayAddress'),
    url(r'deleteAddress/', views.AddressDelete.as_view(), name='deleteAddress'),
    url(r'addAddress/', views.AddressCreate.as_view(), name='addAddress'),
    url(r'updateAddress/', views.update_address, name='updateAddress'),
]