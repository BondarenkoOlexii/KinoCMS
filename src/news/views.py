from django.shortcuts import render, redirect
from src.news.models import NewsStockModel, NewsThourghtImage
from src.common.models import Image
from src.news.forms import NewsForm, SeoForm, NewsImagesFormSet
from src.common.models import SeoBlock


# Create your views here.

def news_stocks(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, prefix='news_stocks')
        seoform = SeoForm(request.POST, prefix='seo')
        image_formset = NewsImagesFormSet(request.POST, request.FILES, prefix='image')  # Імейдж Формсет

        if form.is_valid() and seoform.is_valid() and image_formset.is_valid():
            try:

                seo_instence = seoform.save()  # Зберігаємо seoform в базі данних а seo_instence тепер тримає в собі id цього запису

                news_instence = form.save(commit=False)  # Створюємо об'єкт для збереження, але не закидуємо його в бд

                news_instence.seoblock = seo_instence  # Прив'язуємо запис SEOBLOCK до news

                news_instence.save()  # А тепер уже зберігаємо news в базі данних

                for form in image_formset:
                    image_obj = form.cleaned_data.get("image")  # Тут беремо нашу фотографію
                    upload_image = Image.objects.create(photo=image_obj)  # Тут суємо її в Таблицю з фоточками

                    thourht_instance = form.instance  # Ось це форма нашої проміжної моделі

                    thourht_instance.image = upload_image  # Ось тут наше посилання на картінку з Image ми сунемо в проміжну таблицю

                    thourht_instance.images_info = news_instence  # А це ми сунемо ID тої новини яку раніше зберегли, пов'язучи таблиці між собою

                    thourht_instance.save()  # Зберігаємо

                return redirect('table_news_stocks')

            except Exception as e:
                form.add_error(None, 'Ошибка добавления')
                seoform.add_error(None, 'Ошибка добавления')
        else:
            print(f"Ошибка NewsForm:\n{form.errors.as_text()}")
            print(f"Ошибка SEOForm:\n{seoform.errors.as_text()}")
            print(f"Ошибка ImageFormset:\n {image_formset.errors.as_text()}")
    else:
        form = NewsForm(prefix='news_stocks')
        seoform = SeoForm(prefix='seo')
        image_formset = NewsImagesFormSet(prefix='image')

    context = {
        'news_form': form,
        'seo_form': seoform,
        'image_formset': image_formset,
    }

    return render(request, 'news_stocks.html', context)


def table_news(request):
    items = NewsStockModel.objects.all()
    return render(request, 'table_news_stocks.html', {'items': items})


def table_news_delete(request, pk):
    delete_item = NewsStockModel.objects.get(id=pk)
    delete_item_seo = SeoBlock.objects.get(newsstockmodel=delete_item)

    thourd_images = NewsThourghtImage.objects.filter(images_info=delete_item)

    for item in thourd_images:
        Image.objects.filter(id=item.image_id).delete()


    delete_item_seo.delete()
    thourd_images.delete()
    delete_item.delete()


    return redirect('table_news_stocks')


def update_news(request, pk):
    item = NewsStockModel.objects.get(id=pk)
    seo_item = SeoBlock.objects.get(newsstockmodel=item)
    if request.method == 'POST':

        form = NewsForm(request.POST, instance=item, prefix='news_stocks')
        seoform = SeoForm(request.POST, instance=seo_item, prefix='seo')
        image_formset = NewsImagesFormSet(request.POST, request.FILES, instance=item, prefix="image")

        if form.is_valid() and seoform.is_valid() and image_formset.is_valid():
            seoform_instance = seoform.save()
            form_instance = form.save(commit=False)
            form_instance.seoblock = seoform_instance
            form_instance.save()

            for form in image_formset.forms:
                if form.cleaned_data.get('DELETE'):
                    obj = form.instance
                    if obj.pk:
                        if obj.image:
                            obj.image.delete()
                        obj.delete()


            for form in image_formset:

                if not form.has_changed():                           # Перевіряємо чи трогав щось користувач в формсеті
                        continue                                     # Пропускаємо ітерацію якщо нічого не трогав
                image_file = form.cleaned_data.get('image')          # Якщо, все ж падло щось потрогало то достаємо картінку і тримаємо її

                if image_file:                                        # Перевіряємо чи картінка не пуста

                    if not form.instance.image_id:                   # Якщо вона не пуста і користувач ДОДАВ картинку
                        update_image = Image.objects.create(photo=image_file)                      # Записуємо цю картинку в Image і тримаємо її id

                    else:                                                       # Якщо оказалось що він просто змінив стару картінку
                        form.instance.image.photo = image_file                                                     # Міняємо картінку  на нову

                        form.instance.image.save()                        # Зберігаємо цю картінку

                        update_image = form.instance.image

                    thourgh_form = form.instance

                    thourgh_form.image = update_image

                    thourgh_form.image_info = form_instance

                    thourgh_form.save()

            return redirect('table_news_stocks')
    if request.method == 'GET':
        form = NewsForm(instance=item, prefix='news_stocks')
        seoform = SeoForm(instance=seo_item, prefix='seo')
        image_formset = NewsImagesFormSet(instance=item, prefix="image")

    return render(request, 'news_stocks.html',
                  {'item': item, 'seo_item': seo_item, 'news_form': form, 'seo_form': seoform,
                   'image_formset': image_formset})
