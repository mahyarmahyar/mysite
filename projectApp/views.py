from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


def index_view(request):
    return HttpResponse('home')


def about_view(request):
    return HttpResponse('about')


def contact_view(request):
    return HttpResponse('contact')
