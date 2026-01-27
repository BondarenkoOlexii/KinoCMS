from django import forms
from django.forms import inlineformset_factory

from src.cinema.models import Film, Cinema, Hall, SeoBlock, FilmThourghtImage, CinemaThourghtImage, HallThourghtImage
from src.adminpanel.models.FilmChoise import FilmChoises
class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['name_uk_ua', 'name_ru', 'description_uk_ua', 'description_ru', 'trailer', 'type', 'start_time']

        exclude = ('seoblock', 'image', )

        widgets = {
            'name_uk_ua': forms.TextInput(attrs={'class': 'col-sm-6"'}),
            'name_ru': forms.TextInput(attrs={'class': 'col-sm-6"'}),

            'description_uk_ua': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description_ru': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

            'trailer': forms.URLInput(attrs={'class': 'form-control'}),
            'type': forms.RadioSelect(choices=FilmChoises),
            'start_time': forms.DateInput(attrs={'type': 'date', 'class': 'col-sm-6"'})
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
        model = FilmThourghtImage
        fields = ['image_type']


FilmImagesFormSet = inlineformset_factory(Film, FilmThourghtImage, ImageForm, extra=1, can_delete=True, )


#--------------------------------------------------------------------------------------------------------------------------------------------------

class CinemaForm(forms.ModelForm):
    class Meta:
        model = Cinema
        fields = ['name_uk_ua', 'name_ru', 'discription_uk_ua', 'discription_ru', 'condition_uk_ua', 'condition_ru']

        exclude = ('seoblock', 'image', )

        widgets = {
            'name_uk_ua': forms.TextInput(attrs={'class': 'col-sm-6"'}),
            'name_ru': forms.TextInput(attrs={'class': 'col-sm-6"'}),

            'discription_uk_ua': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'discription_ru': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

            'condition_uk_ua': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'condition_ru': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'type': "file", 'class': 'upload_img'}),
        label="Фотографія"
    )

    class Meta:
        model = CinemaThourghtImage
        fields = ['image_type']


CinemaImagesFormSet = inlineformset_factory(Cinema, CinemaThourghtImage, ImageForm, extra=2, can_delete=True, )

#--------------------------------------------------------------------------------------------------------------------------------------------------

class HallForm(forms.ModelForm):
    class Meta:
        model = Hall
        fields = ['name', 'description']

        exclude = ('seoblock', 'image', )

        widgets = {
            'name': forms.TextInput(attrs={'class': 'col-sm-6"'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class HallImageForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'type': "file", 'class': 'upload_img'}),
        label="Фотографія"
    )

    class Meta:
        model = HallThourghtImage
        fields = ['image_type']


HallImagesFormSet = inlineformset_factory(Hall, HallThourghtImage, HallImageForm, extra=2, can_delete=True, )