import re

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from .models import User, Address, CreditCard

# CURRENTLY ONLY SUPPORTS VISA, AMEX, DISCOVER, AND MASTERCARD
# if you want to add another type, feel free to

# table of regex patterns and the cards that they represent
# source for valid lengths: https://en.wikipedia.org/wiki/Payment_card_number
verificationTable = [("4[0-9]{6,}$", "Visa", [13, 16, 19]),
                     ("3[47][0-9]{5,}$", "AmEx", [15]),
                     ("6(?:011|4|5[0-9]{2})[0-9]{3,}$", "Discover", [16, 17, 18, 19]),
                     ("5[1-5][0-9]{5,}|222[1-9][0-9]{3,}|22[3-9][0-9]{4,}|2[3-6][0-9]{5,}|27[01][0-9]{4,}|2720[0-9]{3,}$", "MasterCard", [16])]

def getCardType(ccn):
    for entry in verificationTable:
        if(re.match(entry[0], ccn)):
            return entry[1]
    return "invalid type"

# iterates through an array and returns a string with all members, separated by ", "
# e.g. createCommaString([1, 2, 3]) = "1, 2, 3"
# used for printing out lengths of cards to help validate
def createCommaString(array):
    final = ""
    for a in range(0, len(array)):
         num = array[a]
         final += str(num)
         if (a != len(array) - 1):
             final += ", "

    return final

# removes spaces and dashes from input, so the user can type like "4444 4444" or "1234-5678"
# has the side affect of allowing weird stuff like "1 2-34 567 8" but as long as the numbers are in proper order nothing is affected
# stuff like that shouldn't happen anyway
def spaceAndDashFix(string):
    stringNew = string.replace(" ", "")
    stringNew = stringNew.replace("-", "")
    return stringNew

# verifies the credit card number using the validation algorithm
def verifyCardNumber(cc):
        ccn = spaceAndDashFix(cc)  # remove all spaces and dashes to allow for typing like "4444 4444" or "1234-5678"
        sum = 0
        doubleMe = True
        for a in range(0, len(ccn)):  # for every character in the input string
            x = ccn[a]
            num = int(x)  # convert the string to int
            if (doubleMe):  # if it's the first/third/fifth...character (index 0, 2, 4...) double it
                if (num >= 5 and num <= 9):  # if doubling the number gives a two-digit number (that is, num >= 5) both digits are added separately
                    num = (2 * num) - 9  # that is given by the function (2 * num) - 9, example: 7 * 2 = 14 -> 1 and 4, 1 + 4 = 5 which is 14 - 9, works for each case
                elif (num >= 0 and num <= 4):
                    num = num * 2  # otherwise it'll give a single-digit number (num < 5)
                else:
                    raise ValueError("this point should not be reached")
                sum += num  # add it to the sum
                doubleMe = False  # the next number must not be doubled
            else:  # if it's the second/fourth/sixth...character (index 1, 3, 5...)
                sum += num  # just add it to the sum as is
                doubleMe = True  # the next number must be doubled

        if sum % 10 == 0:  # if the sum is divisible by 10, the CCN is valid (provided it has a valid type, but that's checked separately)
            return True
        else:  # otherwise it's fake
            return False

class LoginForm(forms.Form):
    nickname = forms.CharField(required=True)
    password = forms.CharField(required=True)

    class Meta:
        fields = ('nickname', 'password')
        model = User

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']

        try:
            User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            raise forms.ValidationError('Sorry that user does not exist.')

        return nickname


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email_address = forms.EmailField(max_length=254, required=True)

    class Meta:
        fields = ("nickname", "email_address", 'first_name', 'last_name', "password1", "password2")
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  #might have issues with python 2

        for field_name in ['password1', 'password2']:
            self.fields[field_name].help_text = None

        self.fields["email_address"].label = "Email Address"
        self.fields["first_name"].label = "First Name"
        self.fields["last_name"].label = "Last Name"
        self.fields["password2"].label = "Password Confirmation"

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']

        if not re.search(r'^\w+$', nickname):
            raise forms.ValidationError('Nickname can only contain alphanumeric characters and underscore.')

        try:
            User.objects.get(nickname=nickname)

        except User.DoesNotExist:
            return nickname

        raise forms.ValidationError('Nickname already exists.')

    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2

            raise forms.ValidationError('Password do not match!')

    def clean_email_address(self):
        email = self.cleaned_data['email_address']

        # check if email address is valid
        if not re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email.lower()):
            raise forms.ValidationError('Email Address is invalid format.')

        # check if email address already exits
        try:
            User.objects.get(email_address=email)
        except User.DoesNotExist:
            return email

        raise forms.ValidationError('Email Address already exists.')


class EditCreditCardForm(ModelForm):
    exp_date = forms.CharField(label = 'Expiration Date')
    cvv = forms.CharField(label = 'CVV')
    owner_name = forms.CharField(label = 'Owner name')

    # verifies the credit card number and type
    def clean_credit_card_number(self):
       cc = self.cleaned_data['credit_card_number']
       if (verifyCardNumber(cc) == False):  # if the card number is invalid, don't even bother
           raise forms.ValidationError('Card number is invalid!')
       else:  # otherwise
           ccn = spaceAndDashFix(cc)  # remove all spaces and dashes to allow for typing like "4444 4444" or "1234-5678"
           for pair in verificationTable:
               if (re.match(pair[0], ccn)):  # if the number matches a regex in the table
                   if (len(ccn) in pair[2]):  # make sure it's got a valid length
                       cardtype = pair[1]
                       return ccn # to keep consistency the "entered" ccn is the space and dash fixed one
                   else:
                       raise forms.ValidationError("Invalid card length! Valid lengths for " + pair[1] + " cards: " + createCommaString(pair[2]))
           else:  # otherwise it's a valid number but it's not an accepted type, alert the users as to which types are supported
               raise forms.ValidationError('Not a valid card type!\nAccepted: Visa, MasterCard, Discover, American Express')

    def clean_exp_date(self):
        ed = self.cleaned_data['exp_date']
        if(re.match("^(0[1-9]|1[0-2])\/([0-9]{2}$)", ed)):
            return ed
        else:
            raise forms.ValidationError("Invalid expiration date! Use format: MM/YY")

    def clean_cvv(self):
        cv = self.cleaned_data['cvv']
        cardtype = "Visa" # HOLDER CODE, TEMPORARY
        if(re.match("^[0-9]{3}$", cv)):
            if(cardtype == "AmEx"):
                #raise forms.ValidationError(str.format("CVV for type {} must be 4 digits", cardtype))
                raise forms.ValidationError("CVV for Amex must be 3 digits")
            else:
                return cv
        elif(re.match("^[0-9]{4}$", cv)):
            if(cardtype != "AmEx"):
                # raise forms.ValidationError(str.format("Cvv for type {} must be 4 digits", cardtype))
                raise forms.ValidationError("CVV for Visa, MasterCard, Discover must be 3 digits")
            else:
                return cv
        else:
            raise forms.ValidationError("Invalid CVV, must be numbers only with 3 or 4 digits depending on card type")

    class Meta:
        model = CreditCard
        fields = ['credit_card_number', 'exp_date', 'cvv', 'owner_name']



class EditUserProfileForm(ModelForm):
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    nickname = forms.CharField(label='Nickname')
    email_address = forms.EmailField(label="Email Address")

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']

        # check if nickname submitted is the same as the current user online
        if nickname == self.instance.nickname:
            return nickname

        # username is different from previous, check if it already exists
        try:
            User.objects.exclude(pk=self.instance.user_id).get(nickname=nickname)
        except User.DoesNotExist:
            return nickname

        raise forms.ValidationError('Nickname already exists.')

    def clean_email_address(self):
        email_address = self.cleaned_data['email_address']

        # check if email address is missing
        if not email_address:
            raise forms.ValidationError('Email Address is missing.')

        # check if email address submitted is the same as the current user online
        if email_address == self.instance.email_address:
            return email_address

        # email address is different from previous, check if it already exits
        try:
            User.objects.exclude(pk=self.instance.user_id).get(email_address=email_address)
        except User.DoesNotExist:
            return email_address

        raise forms.ValidationError('Email Address already exists')

    class Meta:
        model = User
        fields = ['first_name', 'last_name','nickname','email_address']


class AddressForm(ModelForm):
    street_address = forms.CharField(max_length=255, label="Street Address")
    city = forms.CharField(max_length=50, label="City")
    state = forms.CharField(max_length=2, label="State")
    zip_code = forms.CharField(max_length=5, label="Zip Code")

    def clean_zip_code(self):
        zip_code = self.cleaned_data['zip_code']
        if not zip_code.isdigit():
            raise forms.ValidationError('Zip Code can only contains numbers.')

        if len(zip_code) != 5:
            raise forms.ValidationError('Zip Code must have length of 5 digits.')

        return zip_code

    def clean_state(self):
        state = self.cleaned_data['state']
        if not state.isalpha():
            raise forms.ValidationError('State can only contain letters.')

        return state

    class Meta:
        model = Address
        fields = ['street_address', 'city', 'state', 'zip_code']


class ChangePassword(forms.Form):
    current_password = forms.CharField(label='Current Password', widget=forms.PasswordInput(), required=True)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput(), required=True)
    retyped_password = forms.CharField(label='Retype New Password', widget=forms.PasswordInput(), required=True)

    def __init__(self, data= None, user=None, *args, **kwargs):
        self.user = user
        super(ChangePassword, self).__init__(data=data, *args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data['current_password']

        if not self.user.check_password(current_password):
            raise forms.ValidationError('Incorrect current password.')

        return current_password

    def clean(self):
        cleaned_data = self.cleaned_data
        new_password = self.cleaned_data['new_password']
        retyped_password = self.cleaned_data['retyped_password']

        if new_password != retyped_password:
            self.add_error('new_password', 'New password and retyped password do not match.')

        return cleaned_data



