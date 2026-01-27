from django import forms
from django.forms import inlineformset_factory
from src.adminpanel.models.BannerChoise import TypeBanner, DropBox
from src.page.models import Page, MainPage, Banner, BackgroundBanner, SeoBlock, PageThourghtImage, BannerThourghtImage, BackBannerThourghtImage

class MainPageForm(forms.ModelForm):
    class Meta:
        model = MainPage
        fields = ['number_phone', 'seo_text_uk_ua', 'seo_text_ru']

        exclude = ('seoblock', )

        widgets = {
            'number_phone': forms.TextInput(attrs={'class': 'col-sm-6"'}),
            'seo_text_uk_ua': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'seo_text_ru': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PagesForm(forms.ModelForm):

    class Meta:
        model = Page
        fields = ['name_uk_ua', 'name_ru', 'description_uk_ua', 'description_ru', 'type', 'is_active']

        exclude = ('seoblock', 'image', )

        widgets = {
            'name_uk_ua': forms.TextInput(attrs={'class': 'col-sm-6"'}),
            'name_ru': forms.TextInput(attrs={'class': 'col-sm-6"'}),

            'description_uk_ua': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'description_ru': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

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
        widget=forms.FileInput(attrs={'type': "file", 'class': 'add-form-button'}),
        label="Фотографія"
    )

    class Meta:
        model = PageThourghtImage
        fields = ['image_type']


PageImagesFormSet = inlineformset_factory(Page, PageThourghtImage, ImageForm, extra=1, can_delete=True, )




#--------------------------------------------------------------------------------------------------------------------------------------
class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner

        fields = ['type', 'active', 'speed_button']

        exclude = ('image', )

        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'switch__input'}),
            'speed_button': forms.Select(choices=DropBox),
            'type': forms.Select()
        }


class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'type': "file", 'class': 'add-form-button'}),
        label="Фотографія"
    )

    class Meta:
        model = BannerThourghtImage
        fields = ['images_info', 'image_type', 'text', 'url']

        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'url': forms.URLInput(attrs={'class': 'form-control'})

        }

BannerImagesFormSet = inlineformset_factory(Banner, BannerThourghtImage, ImageForm, extra=3, can_delete=True, )


class BackBannerForm(forms.ModelForm):
    class Meta:
        model = BackgroundBanner
        fields = ['is_image', 'background_color']

        exclude = ('image',)

class BackImageForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'type': "file", 'class': 'add-form-button'}),
        label="Фотографія"
    )

    class Meta:
        model = BannerThourghtImage
        fields = ['images_info']

BackBannerImagesFormSet = inlineformset_factory(BackgroundBanner, BackBannerThourghtImage, BackImageForm, extra=1, can_delete=True, )