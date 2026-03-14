from django.http import response

from src.page.models import BannerThourghtImage, BackgroundBanner
from django.conf import settings
from django.utils import translation


def film_ads(request):
    return {'ads': BannerThourghtImage.objects.filter(image_type='stock').order_by('?').first()}

def back_banner(request):
    return {'back_banner': BackgroundBanner.objects.first()}

def set_language(request):
    user_language = request.user.language
    translation.activate(user_language)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, user_language)