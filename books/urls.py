from django.conf.urls import url, include
from . import views


urlpatterns = [
    # /books/
    url(r'^$', views.books, name='books'),

    # /books/id/
    url(r'^(?P<book_id>[0-9]+)/$', views.books_details, name='books_details'),

    # /books/byauthor/id/
    url(r'byauthor/(?P<author_id>[0-9]+)/$', views.by_author, name='by_author'),

    # /books/byauthor/
    url(r'byauthor/$', views.authors, name='authors'),

    # /books/author/id/
    url(r'author/(?P<author_id>[0-9]+)/$', views.author_details, name='author_details'),

    # /books/review/id/
    url(r'review/(?P<book_id>[0-9]+)/$', views.review_book, name='review_book'),

]
