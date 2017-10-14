from django.template import loader
from .models import Book, Author, Review
from .forms import ReviewForm
from purchases.models import PreviousOrder
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import logging

# Create your views here.


def book_search(request):
    queryset = Book.objects.all().order_by("title")
    query = request.GET.get("bookSearch")
    if query:
        queryset = queryset.filter(title__icontains=query)
    context = {
        "queryset": queryset,
    }
    return render(request, 'searchlayout.html', context)


def search_byauthor(request, author_id):
    all_books = Book.objects.filter(author_id=author_id)

    template = loader.get_template('books/listBooks.html')
    context = {
        'all_books': all_books,
    }
    return HttpResponse(template.render(context, request))


#def genre(request):
#    genres = Book.objects.order_by('genre').distinct()
#    context = {
#        'genres': genres,
#    }
#    return render(request, 'genre.html', context)


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
    author = Author.objects.get(pk=book.author_id)
    review = Review.objects.filter(book=book_id)
    template = loader.get_template('books/booksDetails.html')
    context = {
        'book': book,
        'author': author,
        'review':review,
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


