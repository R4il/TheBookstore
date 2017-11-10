from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
from books.models import Book
# Create your views here.


def cart(request, book_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/accounts/signUp/')
    if book_id:
        if 'cart' in request.POST:
            entry, created = Orders.objects.get_or_create(user=request.user, book_id=book_id, defaults={'qty': request.POST['select']})
            entry.save()
        elif 'wishlist' in request.POST:
            entry, created = WishList.objects.get_or_create(user=request.user, book_id=book_id, defaults={'qty': request.POST['select']})
            entry.save()
    return HttpResponseRedirect(f'/books/{book_id}')
