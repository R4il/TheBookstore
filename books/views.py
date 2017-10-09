from django.template import loader
from .models import Book, Author
from django.http import HttpResponse


# Create your views here.
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
    template = loader.get_template('books/booksDetails.html')
    context = {
        'book': book,
        'author': author,
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

