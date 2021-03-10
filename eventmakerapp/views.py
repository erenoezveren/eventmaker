from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    #Home page
    
    response = HttpResponse("Test Home Page") 
    return response
    
def about(request):
    #about page view
    
    
    response = HttpResponse("Test About Page") 
    return response