from django import forms
from .models import Image


class ImageForm(forms.ModelForm):
    """Form for the image model"""
    class Meta:
        model = Image
        fields = ('title', 'image')

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({
            'class': 'form-control',
            'id': 'inputGroupFile04',
            'aria-describedby':'inputGroupFileAddon04',
            'aria-label':'Upload'
        })
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        if not title:
            cleaned_data['title'] = 'Default Title'
        return cleaned_data
