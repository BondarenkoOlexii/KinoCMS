from django.db.models.signals import post_save
from django.dispatch import receiver
from src.page.models import Page, MainPage
from src.cinema.models import Cinema, Hall
from src.common.models import SeoBlock

@receiver(post_save, sender=Page)
@receiver(post_save, sender=MainPage)
@receiver(post_save, sender=Cinema)
@receiver(post_save, sender=Hall)
def create_page_seo(sender, instance, created, **kwargs):
    if created:
        if not instance.seoblock:
            new_seo = SeoBlock.objects.create(
                keyword=f"seo{sender.__name__.lower()}_{instance.id}",
                title="ABC",
                description="ABC",
                url='https://www.google.com'
            )
            instance.seoblock = new_seo
            instance.save()


