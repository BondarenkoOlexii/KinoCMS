from django import forms
from django.forms import inlineformset_factory

from src.news.models import NewsStockModel, SeoBlock, Image, NewsThourghtImage
from src.common.models import ThourghtImage

class NewsForm(forms.ModelForm):

    class Meta:
        model = NewsStockModel
        fields = ['name', 'description', 'trailer', 'is_active']

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
        widget=forms.FileInput,
        label="Фотографія"
    )

    class Meta:
        model = NewsThourghtImage
        fields = ['image_type']


NewsImagesFormSet = inlineformset_factory(NewsStockModel, NewsThourghtImage, ImageForm, extra=1)