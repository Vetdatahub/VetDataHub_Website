from django.shortcuts import render


def datasets(request):
    return render(request,'datasets.html')