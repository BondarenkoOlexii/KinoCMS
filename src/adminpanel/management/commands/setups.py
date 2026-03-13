from django.core.management.base import BaseCommand
from src.page.models import MainPage, Page, Contacts, PageThourghtImage
from src.cinema.models import Cinema, Hall, CinemaThourghtImage
from src.common.models import Image

from django.core.files import File
from pathlib import Path
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.setup_main_page()
        pages = self.setup_pages()
        cinema = self.setup_cinema()
        image = self.setup_image()

        if image:
            self.thourd_cinema_img(image, cinema)
            self.setup_contact_page(image)
            for page in pages:
                self.thourg_pages_image(image, page)

        self.setup_hall(cinema)

        self.stdout.write(self.style.SUCCESS("БАЗОВІ СТОРІНКО СТВОРЕНО"))


    def setup_main_page(self):
        main_page, create = MainPage.objects.get_or_create(id=1,
                                                           defaults={'id': 1, 'number_phone': '+380931111111', 'seo_text': 'ABC'})

    def setup_contact_page(self, img):
        contact_page, create = Contacts.objects.get_or_create(id=1,
                                                              defaults={'id':1, 'name': 'Контакти', 'name_uk':'Контакти', 'adress': 'ABC', 'coordinate': '123', 'image': img, 'image_type': 'logo'})



    def setup_pages(self):
        created_pages = []

        pages = [
            {'id': 2, 'name': 'О кинотеатре', 'name_uk': 'Про Кінотеатр', 'description': 'ABC', 'type' : 'description', 'is_active':True},
            {'id': 3, 'name': 'Реклама', 'name_uk': 'Реклама', 'description': 'ABC', 'type': 'stock', 'is_active': True},
            {'id': 4, 'name': 'VIP - зал', 'name_uk': 'VIP - зал', 'description': 'ABC', 'type': 'vip', 'is_active': True},
            {'id': 5, 'name': 'Детская комната', 'name_uk': 'Дитяча кімната', 'description': 'ABC', 'type': 'child', 'is_active': True},
            {'id': 6, 'name': 'Кафе - Бар', 'name_uk': 'Кафе - Бар', 'description': 'ABC', 'type': 'cafe', 'is_active': True},
        ]

        for page_data in pages:

            page_obj, _ = Page.objects.get_or_create(
                id=page_data.get('id'),
                defaults={
                    'name': page_data['name'],
                    'description': page_data['description'],
                    'type': page_data['type'],
                    'is_active': True,
                }
            )
            created_pages.append(page_obj)
        return created_pages

    def thourg_pages_image(self, img, page):
        PageThourghtImage.objects.get_or_create(images_info=page, image=img, image_type='logo')
    def setup_image(self):
        img = Path(settings.BASE_DIR) / 'src' / 'static' / 'dist' / 'image' / '1.jpg'
        if img.exists():
            with img.open('rb') as f:
                new_image = Image.objects.create()
                new_image.photo.save(img.name, File(f), save=True)

        return new_image


    def thourd_cinema_img(self, img, cinema):
        CinemaThourghtImage.objects.get_or_create(images_info=cinema, image=img, image_type='logo')



    def setup_cinema(self):
        cinema_obj, _ = Cinema.objects.get_or_create(id=1,
                                                     defaults={
                                                    "name": 'Кинотеатр', 'name_uk': 'Кінотеатр', 'discription': 'ABC', 'condition': 'ABC'
                                                     })
        return cinema_obj


    def setup_hall(self, instance):
        hall_obj, _ = Hall.objects.get_or_create(id=1,
                                                 defaults={
                                                 "name": 'Зал 1', "description": 'ABC', 'cinema': instance
                                                 })
