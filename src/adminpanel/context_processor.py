from src.page.models import BannerThourghtImage, BackgroundBanner

def film_ads(request):
    return {'ads': BannerThourghtImage.objects.filter(image_type='stock').order_by('?').first()}

def back_banner(request):
    return {'back_banner': BackgroundBanner.objects.first()}