from src.page.models import BannerThourghtImage

def film_ads(request):
    return {'ads': BannerThourghtImage.objects.filter(image_type='main').order_by('?').first()}