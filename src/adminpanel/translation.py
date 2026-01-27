from modeltranslation.translator import register, TranslationOptions
from src.cinema.models import Film, Cinema, Hall
from src.news.models import NewsStockModel
from src.user.models import User
from src.page.models import Page, MainPage


@register(Film)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Cinema)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'discription', 'condition')


@register(Hall)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(NewsStockModel)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(MainPage)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('seo_text',)

@register(Page)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


