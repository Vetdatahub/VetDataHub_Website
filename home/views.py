from django.shortcuts import render,redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from home.forms import ContactForm

# Create your views here.
def home(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            try:
                send_mail(subject, message, email, ['vetdatahub@gmail.com'], name)
            except BadHeaderError:
                return HttpResponse("Invalid header found")
            return redirect("home")

    return render(request,"home/home.html",context={"form": form})

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'about.html')