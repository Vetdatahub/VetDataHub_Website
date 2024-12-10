from django.forms import ModelForm
from datasets.models import Dataset, DatasetVersion, Tag, Rating
from django import forms


class DatasetUploadForm(forms.ModelForm):
    # Include DatasetVersion fields
    file = forms.FileField(label="Dataset File", required=True)
    version_description = forms.CharField(
        label="Version Description",
        required=False,
    )

    class Meta:
        model = Dataset
        fields = [
            "name",
            "description",
            "tags",
            "dataset_type",
        ]
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
            "description": forms.Textarea(attrs={"rows": 5}),
        }

    def save(self, commit=True, user=None):
        # Save the Dataset instance
        dataset = super().save(commit=commit)

        # Save the associated DatasetVersion instance
        if commit:
            DatasetVersion.objects.create(
                dataset=dataset,
                version_number=1,  # First version for a new dataset
                description=self.cleaned_data.get("version_description"),
                file=self.cleaned_data["file"],
                created_by=user,
                is_latest=True,
            )

        return dataset


class DatasetVersionForm(forms.ModelForm):
    class Meta:
        model = DatasetVersion
        fields = ["file", "description"]
    def __init__(self,*args,**kwargs):
        self.user =  kwargs.pop('user')
        self.dataset =  kwargs.pop('dataset')
        super().__init__(*args, **kwargs)


    def save(self,commit=True):
        version = super().save(commit=False)
        version.created_by = self.user
        version.dataset = self.dataset
        version.save()
        return version


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ["rating", "review"]
        widgets = {
            "rating": forms.RadioSelect(
                choices=[(i, str(i)) for i in range(1, 11)]
            ),
            "review": forms.Textarea(attrs={"rows": 3}),
        }
    def __init__(self,*args,**kwargs):
        self.user =  kwargs.pop('user')
        self.dataset =  kwargs.pop('dataset')
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        # Associate rating with the current user and dataset
        rating = super().save(commit=False)
        rating.user = user
        rating.dataset = dataset
        rating.save()
        return rating


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Enter tag name"}),
        }
