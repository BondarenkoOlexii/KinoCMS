from django.shortcuts import render, redirect, get_object_or_404
from src.page.models import Page, Banner, BackgroundBanner
from src.common.models import Image, SeoBlock
from src.page.forms import PagesForm, ImageForm, SeoForm, BannerForm, PageImagesFormSet, BannerImagesFormSet, MainPage, MainPageForm

# Create your views here.

def page(request):
    if request.method == 'POST':
        form = PagesForm(request.POST, prefix='page')
        seoform = SeoForm(request.POST, prefix='seo')
        image_formset = PageImagesFormSet(request.POST, request.FILES, prefix='image')

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

                    return redirect('table_news_stocks')
            except Exception as e:
                form.add_error(None, 'Ошибка добавления')
                seoform.add_error(None, 'Ошибка добавления')

        else:
            print(f"Ошибка PageForm:\n {form.errors.as_text()}")
            print(f"Ошибка SeoForm:\n {seoform.errors.as_text()}")
            print(f"Ошибка ImageFormset:\n {image_formset.errors}")

    else:
        form = PagesForm(prefix='page')
        seoform = SeoForm(prefix='seo')
        image_formset = PageImagesFormSet(prefix='image')

    context = {'pageform': form, 'seoform': seoform, 'image_formset': image_formset}

    return render(request, 'page.html', context)

def table_page(request):
    items = list(Page.objects.all())
    main_item = list(MainPage.objects.all())
    items += main_item
    return render(request, 'pages_table.html', {'items': items})

def delete_pages(request, pk):
    delete_item = Page.objects.get(id=pk)
    delete_item_seo = SeoBlock.objects.get(page=delete_item)

    thourd_images = ImageForm.objects.filter(images_info=delete_item)

    for item in thourd_images:
        Image.objects.filter(id=item.image_id).delete()

    delete_item_seo.delete()
    thourd_images.delete()
    delete_item.delete()

def update_pages(request, pk):
    item = Page.objects.get(pk=pk)
    seo_item = SeoBlock.objects.get(page=item)
    if request.method == 'POST':

        form = PagesForm(request.POST, instance=item, prefix='page')
        seoform = SeoForm(request.POST, instance=seo_item, prefix='seo')
        image_formset = PageImagesFormSet(request.POST, request.FILES, instance=item, prefix="image")

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

                    thourgh_form.images_info = page_instance

                    thourgh_form.save()

            return redirect('table_news_stocks')
    else:
        form = PagesForm(instance=item, prefix='page')
        seoform = SeoForm(instance=seo_item, prefix='seo')
        image_formset = PageImagesFormSet(instance=item, prefix="image")

    return render(request, 'page.html',
                  {'item': item, 'seo_item': seo_item, 'pageform': form, 'seoform': seoform, 'image_formset': image_formset})


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def update_main_page(request, pk):

    item = get_object_or_404(MainPage, pk=pk)
    seo_item = SeoBlock.objects.get(mainpage=item)

    if request.method == "POST":
        form = MainPageForm(request.POST, prefix='form', instance=item)
        seoform = SeoForm(request.POST, instance=seo_item, prefix='seo')

        if form.is_valid() and seoform.is_valid():
            seo_instance = seoform.save()

            form_instance = form.save(commit=False)

            form_instance.seoblock = seo_instance

            form_instance.save()

            return redirect('table_pages')

    if request.method == "GET":
        form = MainPageForm(instance=item, prefix='form')
        seoform = SeoForm(instance=seo_item, prefix='seo')

    return render(request, 'main_page.html', {'form': form, 'main_item':item, 'seoform':seoform, 'seo_item':seo_item})


























#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def banner(request):
    initial_data = [
        {'image_type': 'logo'},
        {'image_type': 'gallery'}
    ]

    obj, _ = Banner.objects.get_or_create(id=1)

    if request.method == 'POST':
        print("REQUST POST")
        banner_form = BannerForm(request.POST, instance=obj, prefix='banner')
        banner_image_formset = BannerImagesFormSet(request.POST, request.FILES, instance=obj, prefix="image")

        if banner_form.is_valid() and banner_image_formset.is_valid():
            print("VSE VALID")
            form_instance = banner_form.save()

            for form in banner_image_formset.forms:
                if form.cleaned_data.get('DELETE'):
                    obj = form.instance
                    if obj.pk:
                        if obj.image:
                            obj.image.delete()
                        obj.delete()

            for form in banner_image_formset:

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

                    thourgh_form.image_info = form_instance

                    thourgh_form.save()

            return redirect('banner')
        else:
            print(banner_form.errors)
            print(banner_image_formset.errors)

    if request.method == 'GET':
        banner_form = BannerForm(instance=obj, prefix='banner')
        banner_image_formset = BannerImagesFormSet(instance=obj, initial=initial_data, prefix="image")

    return render(request, 'banner.html',
                  {'item': obj, 'form': banner_form,
                   'image_formset': banner_image_formset})


def backbanner(request):
    pass