from django.template import loader
from .models import Book, Author, Review
from .forms import ReviewForm
from purchases.models import PreviousOrder
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, CreateView, RedirectView, FormView, UpdateView
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import transaction

import logging

# Create your views here.


def book_search(request):
    queryset = Book.objects.all()
    query = request.GET.get("bookSearch")
    if query:
        queryset = queryset.filter(title__icontains=query)

    context = {
        "queryset": queryset,
    }

    return render(request, 'searchlayout.html', context)


def books(request):
    all_books = Book.objects.all()
    template = loader.get_template('books/listBooks.html')
    context = {
        'all_books': all_books,
    }
    return HttpResponse(template.render(context, request))


def authors(request):
    all_authors = Author.objects.all().order_by('last')
    template = loader.get_template('books/allTheAuthors.html')
    context = {
        'all_authors': all_authors,
    }
    return HttpResponse(template.render(context, request))


def books_details(request, book_id):
    book = Book.objects.get(pk=book_id)
    request.session['book_id'] = book_id
    author = Author.objects.get(pk=book.author_id)
    reviews = Review.objects.filter(book=book_id)
    if len(reviews):
        user_rating = 0
        for review in reviews:
            user_rating += review.rating
        user_rating = round(user_rating / len(reviews), 2)
    else:
        user_rating = 'Unreviewed'
        
    template = loader.get_template('books/booksDetails.html')
    context = {
        'book': book,
        'author': author,
        'reviews': reviews,
        'user_rating': user_rating,
    }
    return HttpResponse(template.render(context, request))


def author_details(request, author_id):
    author = Author.objects.get(pk=author_id)
    template = loader.get_template('books/authorDetails.html')
    context = {
        'author': author,
    }
    return HttpResponse(template.render(context, request))


def by_author(request, author_id):
    all_books = Book.objects.filter(author_id=author_id)

    template = loader.get_template('books/listBooks.html')
    context = {
        'all_books': all_books,
    }
    return HttpResponse(template.render(context, request))


def review_book(request, book_id):
    user = request.user
    book = Book.objects.get(pk=book_id)
    order = PreviousOrder.objects.filter(user=user.user_id, book=book_id)
    if len(order) == 0:
        return render(request, 'reviewDenied.html')
    else:
        if request.method == 'POST':
            review = Review.objects.filter(user=user.user_id, book=book_id)
            form = ReviewForm(data=request.POST)
            if form.is_valid():
                if len(review):
                    Review.objects.filter(user=user.user_id, book=book_id).delete()

                final = form.save(commit=False)
                final.user = user
                final.book = book
                final.save()
                return render(request, 'reviewSuccessful.html', {'book': book})
            else:
                return render(request, 'formProblem.html', {'error': form.errors, 'book': book})
        else:
            form = ReviewForm()
            return render(request, 'reviewForm.html', {'form': form})


class ReviewBookView(CreateView):
    model = Review
    form_class = ReviewForm

    def form_valid(self, form):
        if 'book_id' in self.request.session:
            book_id = self.request.session['book_id']
        else:
            return
        book = Book.objects.get(pk=book_id)
        user = self.request.user
        order = PreviousOrder.objects.filter(user=user.user_id, book=book_id)
        if len(order) == 0:
            return render(self.request, 'reviewDenied.html')
        final = form.save(commit=False)
        with transaction.atomic():
            try:
                obj = Review.objects.get(user=user, book=book)
                obj.rating = final.rating
                obj.title = final.title
                obj.body = final.body
                obj.anonymous = final.anonymous
                obj.save()
            except Review.DoesNotExist:
                obj = Review(user=user, book=book, rating=final.rating,
                             title=final.title, body=final.body, anonymous=final.anonymous)
                obj.save()
            return HttpResponseRedirect(f'/books/{book_id}')
        
    def get_success_url(self):
        messages.success(self.request, 'Review was added to db.')
        return redirect('/books/')

