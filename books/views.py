from django.template import loader
from .models import Book, Author, Review, Genre
from .forms import ReviewForm
from purchases.models import PreviousOrder
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import DeleteView, CreateView, RedirectView, FormView, UpdateView
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import transaction
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import logging

# Create your views here.


def book_search(request):
    queryset = Book.objects.all().order_by("title")
    authorset = Author.objects.all().order_by("last")
    query = request.GET.get("bookSearch")
    if query:
        queryset = queryset.filter(title__icontains=query)
        authorset = authorset.filter(Q(last__icontains=query) | Q(first__icontains=query))
    context = {
        "queryset": queryset,
        "authorset": authorset,
    }
    return render(request, 'searchlayout.html', context)


def search_byauthor(request, author_id):
    all_books = Book.objects.filter(author_id=author_id)

    template = loader.get_template('books/listBooks.html')
    context = {
        'all_books': all_books,
    }
    return HttpResponse(template.render(context, request))


def genre(request):
    genres = Genre.objects.all().order_by("genre")
    context = {
        'genres': genres,
    }
    return render(request, 'genre.html', context)


def booksbygenre(request, genre_id):
    all_books = Book.objects.filter(genre_id=genre_id).order_by("title")
    paginator = Paginator(all_books, 10)  # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        books = paginator.page(paginator.num_pages)

    context = {
        "all_books": books
    }

    return render(request, "books/listBooks.html", context)


def bestsellers(request):
    all_books = Book.objects.filter(best_seller__icontains='Y').order_by("title")
    paginator = Paginator(all_books, 10) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        books = paginator.page(paginator.num_pages)

    context = {
        "all_books": books
    }

    return render(request, "books/listBooks.html", context)


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

def authorsalpha(request):#tobe done
    all_authors = Author.objects.all().order_by('last')
    template = loader.get_template('books/allTheAuthors.html')
    authors = Author.objects.filter(name__iregex=r"[[:<:]]{0}".format(searchStr))
    context = {
        'authoralpha': authoralpha,
    }
    return HttpResponse(template.render(context, request))


def books_details(request, book_id):
    book = Book.objects.get(pk=book_id)
    request.session['book_id'] = book_id
    author = Author.objects.get(pk=book.author_id)
    reviews = Review.objects.filter(book=book_id)
    if request.user.is_anonymous:
        order = ''
    else:
        order = PreviousOrder.objects.filter(user=request.user, book=book_id)
    if len(order) == 0:
        request.session['purchased'] = False
    else:
        request.session['purchased'] = True
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
        'purchased': request.session['purchased'],
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


def review_denied(request):
    return render(request, 'reviewDenied.html')


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

