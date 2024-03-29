from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.generic import DeleteView, CreateView, RedirectView, FormView, UpdateView
from django.contrib.auth.forms import PasswordChangeForm
from .forms import EditUserProfileForm, EditCreditCardForm, UserCreateForm, AddressForm, LoginForm, ChangePassword
from .models import User, CreditCard, Address
from django.contrib import messages


#########################################################################################################
##                                   USER FUNCTIONS                                                   ##
########################################################################################################

@csrf_protect
def login_view(request):
    next = request.POST.get('next', '/')
    form = LoginForm

    if request.method == 'POST':

        username = request.POST['nickname']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        # if we have a user object, credentials correct
        if user:
            # check to see if account is active
            if user.is_active:
                # if account is active login the user and send the user back to homepage
                login(request, user)
                current_user = request.user

            # no user with matching credentials
        else:
            # bad login credentials were provided
            messages.error(request, 'Sorry the credentials you input, were incorrect.')
            return render(request, 'invalidLogin.html')
        
        return redirect('/')


##COMMENTED OUT TO PREVENT CRASH
# ##Needs to be done
# # create cart for new users or customers with previous cart already purchased
# def create_shopping_cart(user_id):
#     return user_id
#
# ##Needs to be done
# # create a future order for new users who login in to website
# def create_future_order(user_id):
#     return user_id


@csrf_protect
def manage_account(request):
    online_user = request.user
    user = User.objects.get(pk=online_user.user_id)
    form = EditUserProfileForm(request.POST or None, initial={'first_name': online_user.first_name,
                                                    'last_name': online_user.last_name, 'nickname': online_user.nickname,
                                                    'email_address': online_user.email_address}, instance=request.user)

    if request.method == 'POST':
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.nickname = form.cleaned_data['nickname']
            user.email_address = form.cleaned_data['email_address']

            user.save()

            messages.success(request, 'User information changes have been successfully saved.')

            return HttpResponseRedirect(reverse('index'))

    else:
        form = EditUserProfileForm(instance=online_user)

    return render(request, "accounts/manageAccount.html", {'form': form})


class SignUpView(CreateView):
    form_class = UserCreateForm
    model = User
    template_name = "accounts/signUp.html"
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        new_user = form.save()
        messages.info(self.request, 'Thanks for registering. You may now login.')

        # after the new user is created, login the user
        new_user = authenticate(username=form.cleaned_data['nickname'], password=form.cleaned_data['password1'])
        login(self.request, new_user)

        ##COMMENTED OUT TO PREVENT CRASH
        # # create a new shopping cart and add id to session
        # shopping_cart = create_shopping_cart(self.request.user.user_id)
        # self.request.session['orderId'] = shopping_cart.id
        #
        # # create a new future cart and add id to session
        # future_cart = create_future_order(self.request.user.user_id)
        # self.request.session['fOrderId'] = future_cart.id

        return super(SignUpView, self).form_valid(form)

class LogoutView(RedirectView):
    url = reverse_lazy("index")

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Successfully logged out.')
        return super().get(request, *args, **kwargs) #might have issues with python 2

@csrf_protect
def change_password(request):
    form = PasswordChangeForm(user = request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('index'))
        else:
            messages.error(request, 'Please correct the error below.')
            args = {'form': form}
            return render(request, 'accounts/change_password.html', args)
    return render(request, 'accounts/change_password.html', {'form': form})

#########################################################################################################
##                                   CREDIT CARD FUNCTIONS                                             ##
########################################################################################################

def display_cc(request):
    online_user_id = request.user.user_id
    credit_cards = CreditCard.objects.filter(user_id=online_user_id)
    return render(request, 'accounts/displaycc.html', {'credit_cards': credit_cards})

class CreditCardUpdate(UpdateView):
    model = CreditCard
    form_class = EditCreditCardForm
    template_name_suffix = '_update_form'

    def get_success_url(self):
        messages.success(self.request, 'Credit card info was successfully removed.')
        return reverse('accounts:displaycc')

    def get_object(self):
        creditcard_id = self.request.GET.get('cc_id')
        return get_object_or_404(CreditCard, pk=creditcard_id)

class CreateCreditCardView(CreateView):
    model = CreditCard
    form_class = EditCreditCardForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(CreateCreditCardView, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'CCN profile was successfully created.')
        return reverse('accounts:displaycc')


class CreditCardDelete(DeleteView):
    model = CreditCard

    def get_success_url(self):
        messages.success(self.request, 'Credit card info was successfully removed.')
        return reverse('accounts:displaycc')

    def get_object(self):
        cc_id = self.request.POST.get('cc_id')
        return get_object_or_404(CreditCard, pk=cc_id)

#########################################################################################################
##                                   ADDRESS FUNCTIONS                                                 ##
########################################################################################################

def display_address(request):
    online_user_id = request.user.user_id
    addresses = Address.objects.filter(user_id=online_user_id)
    return render(request, 'accounts/displayAddresses.html', {'addresses': addresses})

class AddressUpdate(UpdateView):
    model = Address
    fields = ['street_address', 'city', 'state', 'zip_code']
    template_name_suffix = '_update_form'
    def get_success_url(self):
        messages.success(self.request, 'Address was successfully edited.')
        return reverse('accounts:displayAddress')

    def get_object(self):
        address_id = self.request.GET.get('addr_id')
        return get_object_or_404(Address, pk=address_id)

class AddressDelete(DeleteView):
    model = Address

    def get_success_url(self):
        messages.success(self.request, 'Address was successfully removed.')
        return reverse('accounts:displayAddress')

    def get_object(self):
        address_id = self.request.POST.get('addr_id')
        return get_object_or_404(Address, pk=address_id)

class AddressCreate(CreateView):
    template_name = 'accounts/addAddress.html'
    model = Address
    form_class = AddressForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return super(AddressCreate, self).form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Address was successfully created.')
        return reverse('accounts:displayAddress')



