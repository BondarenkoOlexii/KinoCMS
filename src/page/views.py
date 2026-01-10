from django.shortcuts import render, redirect
from src.page.models import Page, PageThourghtImage
from src.common.models import Image, SeoBlock
from src.page.forms import PagesForm, ImageForm, SeoForm

# Create your views here.

def page(request):
    if request.method == 'POST':
        form = PagesForm(request.POST, prefix='page')
        seoform = SeoForm(request.POST, prefix='seo')
        image_formset = ImageForm(request.POST, request.FILES, prefix='image')

        if form.is_valid() and seoform.is_valid() and image_formset.is_valid():
            try:
                seo_instance = seoform.save()

                page_instance = form.save(commit=False)

                page_instance.seoblock = seo_instance

                page_instance.save()

                for form in image_formset:
                    image_obj = form.cleaned_data.get('image')
                    upload_img = Image.objects.create(photo=image_obj)

                    thourgh_form = form.instance

                    thourgh_form.image = upload_img

                    thourgh_form.images_info = page_instance

                    thourgh_form.save()
            except Exception as e:
                form.add_error(None, 'Ошибка добавления')
                seoform.add_error(None, 'Ошибка добавления')

        else:
            print(f"Ошибка PageForm:\n {form.errors.as_text()}")
            print(f"Ошибка SeoForm:\n {seoform.errors.as_text()}")
            print(f"Ошибка ImageFormset:\n {image_formset.errors.as_text()}")

    else:
        form = PagesForm(prefix='page')
        seoform = SeoForm(prefix='seo')
        image_formset = ImageForm(prefix='image')

    context = {'pageform': form, 'seoform': seoform, 'image_formset': image_formset}

    return render(request, 'page.html', context)

def table_page(request):
    items = Page.objects.all()
    return render(request, 'pages_table.html', {'items': items})
def delete_pages(request, pk):
    delete_item = Page.objects.get(id=pk)
    delete_item_seo = SeoBlock.objects.get(newsstockmodel=delete_item)

    thourd_images = ImageForm.objects.filter(images_info=delete_item)

    for item in thourd_images:
        Image.objects.filter(id=item.image_id).delete()

    delete_item_seo.delete()
    thourd_images.delete()
    delete_item.delete()

def update_pages(request, pk):
    item = Page.objects.get(id=pk)
    seo_item = SeoBlock.objects.get(newsstockmodel=item)
    if request.method == 'POST':

        form = PagesForm(request.POST, instance=item, prefix='news_stocks')
        seoform = SeoForm(request.POST, instance=seo_item, prefix='seo')
        image_formset = ImageForm(request.POST, request.FILES, instance=item, prefix="image")

        if form.is_valid() and seoform.is_valid() and image_formset.is_valid():

            seo_instance = seoform.save()

            page_instance = form.save(commit=False)

            page_instance.seoblock = seo_instance

            page_instance.save()

            for form in image_formset.forms:
                if form.cleaned_data.get('DELETE'):
                    obj = form.instance
                    if obj.pk:
                        if obj.image:
                            obj.image.delete()
                        obj.delete()

            for form in image_formset:

                if not form.has_changed():  # Перевіряємо чи трогав щось користувач в формсеті
                    continue  # Пропускаємо ітерацію якщо нічого не трогав

                image_file = form.cleaned_data.get('image')  # Якщо, все ж падло щось потрогало то достаємо картінку і тримаємо її

                if image_file:  # Перевіряємо чи картінка не пуста

                    if not form.instance.image_id:  # Якщо вона не пуста і користувач ДОДАВ картинку
                        update_image = Image.objects.create(photo=image_file)  # Записуємо цю картинку в Image і тримаємо її id

                    else:  # Якщо оказалось що він просто змінив стару картінку
                        form.instance.image.photo = image_file  # Міняємо картінку  на нову

                        form.instance.image.save()  # Зберігаємо цю картінку

                        update_image = form.instance.image

                    thourgh_form = form.instance

                    thourgh_form.image = update_image

                    thourgh_form.image_info = page_instance

                    thourgh_form.save()

            return redirect('table_news_stocks')
    if request.method == 'GET':
        form = PagesForm(instance=item, prefix='news_stocks')
        seoform = SeoForm(instance=seo_item, prefix='seo')
        image_formset = ImageForm(instance=item, prefix="image")

    return render(request, 'news_stocks.html',
                  {'item': item, 'seo_item': seo_item, 'pageform': form, 'seoform': seoform, 'image_formset': image_formset})