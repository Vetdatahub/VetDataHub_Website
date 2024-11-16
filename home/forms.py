from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label="Name", required=True,widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "display name",
            }
        ),)
    email = forms.EmailField(label="Email", required=True,widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
                "placeholder": "email",
            }
        ),)
    subject = forms.CharField(label="Subject", required=True,widget=forms.TextInput(
            attrs={
                "class": "w-full px-4 py-2 border rounded-lg",
            }
        ),)
    message = forms.CharField(label="Message", required=True,widget=forms.Textarea(
            attrs={
                "class":"w-full px-4 py-2 border rounded-lg",

            }
        ),)
