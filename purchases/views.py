from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import *
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


def display_cart(request):
    user = request.user.user_id
    user_cart = Orders.objects.filter(user_id=user)
    for item in user_cart:
        item_price = item.book.price * item.qty
        item.price = item_price
    return render(request, 'displayCart.html', {'cart': user_cart})


def display_wishlist(request):
    user = request.user.user_id
    wishlist = WishList.objects.filter(user_id=user)
    for item in wishlist:
        item_price = item.book.price * item.qty
        item.price = item_price
    return render(request, 'displayWishlist.html', {'wishlist': wishlist})


def checkout(request):
    user = request.user.user_id
    user_cart = Orders.objects.filter(user_id=user)
    for item in user_cart:
        item.delete()
        order, created = PreviousOrder.objects.get_or_create(book=item.book, user=item.user, qty=item.qty)
        order.save()
    user_cart.delete()
    return HttpResponseRedirect('/books')


def drop(request, book_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/accounts/signUp/')
    if book_id:
        entry = Orders.objects.get(user=request.user, book_id=book_id)
        entry.delete()
    return HttpResponseRedirect(f'/cart')


def drop_wishlist(request, book_id):
    if request.user.is_anonymous:
        return HttpResponseRedirect('/accounts/signUp/')
    if book_id:
        entry = WishList.objects.get(user=request.user, book_id=book_id)
        entry.delete()
    return HttpResponseRedirect(f'/cart/wishlist')
