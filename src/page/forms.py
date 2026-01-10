from django import forms
from django.forms import inlineformset_factory

from src.page.models import Page, SeoBlock, PageThourghtImage


class PagesForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ['name', 'description', 'type', 'is_active']

        exclude = ('seoblock', 'image', )

        widgets = {
            'name': forms.TextInput(attrs={'class': 'col-sm-6"'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'trailer': forms.URLInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'switch__input'})
        }


class SeoForm(forms.ModelForm):
    class Meta:
        model = SeoBlock
        fields = ['url', 'title', 'keyword', 'description']

        widgets = {
            'url': forms.URLInput(attrs={'class': 'col-sm-6', 'placeholder': 'URL'}),
            'title': forms.TextInput(attrs={'class': 'col-sm-6', 'placeholder': 'Title'}),
            'keyword': forms.TextInput(attrs={'class': 'col-sm-6', 'placeholder': 'word'}),
            'description': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'form-control', 'placeholder': 'Description'})
        }



class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'type': "file", 'class': 'upload_img'}),
        label="Фотографія"
    )

    class Meta:
        model = PageThourghtImage
        fields = ['image_type']


NewsImagesFormSet = inlineformset_factory(Page, PageThourghtImage, ImageForm, extra=1, can_delete=True, )