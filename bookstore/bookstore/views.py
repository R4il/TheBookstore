from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect


def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')



