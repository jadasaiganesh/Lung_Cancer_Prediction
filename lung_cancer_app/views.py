from django.shortcuts import render
from django.http import HttpResponse

def homepage(request):
    """ Render the homepage """
    return render(request, 'homepage.html')

def about(request):
    """ Render an about page (optional) """
    return render(request, 'about.html')

def contact(request):
    """ Render a contact page (optional) """
    return render(request, 'contact.html')

def health_check(request):
    """ Health check endpoint to verify server is running """
    return HttpResponse("Server is running successfully!")
