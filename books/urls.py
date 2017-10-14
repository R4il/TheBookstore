from django.conf.urls import url, include
from .views import *


urlpatterns = [
    # /books/
    url(r'^$', books, name='books'),

    # /books/id/
    url(r'^(?P<book_id>[0-9]+)/$', books_details, name='books_details'),

    # /books/byauthor/id/
    url(r'byauthor/(?P<author_id>[0-9]+)/$', by_author, name='by_author'),

    # /books/byauthor/
    url(r'byauthor/$', authors, name='authors'),

    # /books/author/id/
    url(r'author/(?P<author_id>[0-9]+)/$', author_details, name='author_details'),

    # /books/review/id/
    url(r'review/(?P<book_id>[0-9]+)/$', ReviewBookView.as_view(), name='review_book'),
    
    url(r'review_denied/', review_denied, name='review_denied'),
    
]
