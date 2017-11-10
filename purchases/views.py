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


def displayCart(request):
    user = request.user.user_id
    userCart = Orders.objects.filter(user_id=user)
    for item in userCart:
        itemPrice = item.book.price * item.qty
        item.price = itemPrice
    return render(request, 'displayCart.html', {'cart': userCart})


def checkout(request):
    user = request.user.user_id
    userCart = Orders.objects.filter(user_id=user)
    for item in userCart:
        item.delete()
        order, created = PreviousOrder.objects.get_or_create(book=item.book, user=item.user, qty=item.qty)
        order.save()
    userCart.delete()
    return HttpResponseRedirect('/books')
