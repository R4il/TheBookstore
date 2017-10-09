from django.conf.urls import url
from django.contrib import admin
from .views import (
    posts_home,
    book_detail
)

urlpatterns = [
    url(r'^$', posts_home, name='search'),
    url(r'^(?P<id>\d+)/$', book_detail, name='book_detail'),
]