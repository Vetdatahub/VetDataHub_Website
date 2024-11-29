from django import forms
from community.models import Discussion, Comment


class DiscussionForm(forms.ModelForm):
    """
    Form to create or update a discussion.
    """

    class Meta:
        model = Discussion
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter discussion title",
                }
            ),
        }


class CommentForm(forms.ModelForm):
    """
    Form to create a comment on a discussion.
    """

    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Write your comment here",
                }
            ),
        }
