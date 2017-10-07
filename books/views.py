from django.template import loader
from .models import Book, Author
from django.http import HttpResponse


# Create your views here.
def search(request):
    all_books = Book.objects.all()
    template = loader.get_template('books/index.html')
    context = {
        'all_books': all_books,
    }
    return HttpResponse(template.render(context, request))
