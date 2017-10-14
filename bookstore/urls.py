"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import books
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r"^books/", include("books.urls")),
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('send_email.urls')),
    url(r'search', books.views.book_search, name='search'),
    url(r'author/id/(?P<author_id>[0-9]+)/$', books.views.search_byauthor, name='search_byauthor'),
    # url(r'genre', books.views.genre, name='genre'), still working on this
]
