from django.shortcuts import render

# Create your views here.
def analytics(request):
    return render(request,'analytics.html')