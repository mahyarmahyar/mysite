from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from projectApp.forms import ContactForm, NewsletterForm
from django.contrib import messages


def index_view(request):
    return render(request, 'website/index.html')


def about_view(request):
    return render(request, 'website/about.html')


def elements_view(request):
    return render(request, 'website/elements.html')


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'We Received Your Massage')
        else:
            messages.error(request, 'An error occurred')
    form = ContactForm()
    return render(request, 'website/contact.html', {'form': form})


def newsletter_view(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form. is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')
