from django.shortcuts import render, redirect, get_object_or_404
from src.page.models import Page, Banner, BackgroundBanner
from src.common.models import Image, SeoBlock
from src.page.forms import PagesForm, ImageForm, SeoForm, BannerForm, PageImagesFormSet, BannerImagesFormSet, MainPage, MainPageForm, BackBannerForm, BackBannerImagesFormSet, Contacts, ContactImagesFormSet, ContactForm

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
    contact_item = list(Contacts.objects.filter(id=1))
    items += main_item
    items += contact_item
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



def update_contact_page(request, pk):
    item = get_object_or_404(Contacts, pk=pk)
    seo_item = SeoBlock.objects.get(contacts=item)

    if request.method == "POST":
        seo_form = SeoForm(request.POST, prefix='seo', instance=seo_item)
        image_formset = ContactImagesFormSet(request.POST, request.FILES, prefix='image', queryset=Contacts.objects.filter(seoblock=seo_item))

        if seo_form.is_valid() and image_formset.is_valid():
            print("Vse Valid")
            print(request.POST)
            seo_intanse = seo_form.save()

            for form in image_formset:
                instance = form.save(commit=False)
                instance.seoblock = seo_intanse

                image_file = form.cleaned_data.get('image')
                if image_file:
                    if not instance.image_id:
                        instance.image = Image.objects.create(photo=image_file)
                    else:
                        instance.image.photo = image_file
                        instance.image.save()
                if instance.image_id:
                    instance.save()

            return redirect('table_pages')
        else:
            print(seo_form.errors)
            print(image_formset.errors)
    else:
        seo_form = SeoForm(prefix='seo', instance=seo_item)
        image_formset = ContactImagesFormSet(prefix='image', queryset=Contacts.objects.filter(seoblock=seo_item))


    context = {'item': item, 'seo_item': seo_item, 'seoform': seo_form, 'image_formset': image_formset}

    return render(request, 'contact_page.html', context)
















#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def work_formset(formset, img_type, main_obj):
    print(img_type, "START", len(formset.forms))

    for form in formset.forms:
        if form.cleaned_data.get('DELETE'):
            obj = form.instance
            if obj.pk:
                if obj.image:
                    obj.image.delete()
                obj.delete()

    banner_instance = formset.save(commit=False)

    for form in formset:
        print(form)
        if form.cleaned_data and not form.cleaned_data.get('DELETE'):
            image_file = form.cleaned_data.get('image')


            if not form.instance.pk and not image_file:
                continue

            if not form.has_changed() and form.instance.pk:
                continue

            instance = form.save(commit=False)

            if image_file:
                if not instance.image_id:
                    instance.image = Image.objects.create(photo=image_file)
                else:
                    instance.image.photo = image_file
                    instance.image.save()

            instance.image_info = main_obj
            instance.image_type = img_type
            instance.save()



#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def banner(request):

    banner_obj, _ = Banner.objects.get_or_create(id=1)
    back_banner_obj, _ = BackgroundBanner.objects.get_or_create(id=1)

    stock_queryset = banner_obj.bannerthourghtimage_set.filter(image_type='stock')
    main_queryset = banner_obj.bannerthourghtimage_set.filter(image_type='main')

    banner_form = BannerForm(instance=banner_obj, prefix='banner')
    back_banner_form = BackBannerForm(instance=back_banner_obj, prefix='backbanner')

    main_formset = BannerImagesFormSet(instance=banner_obj, prefix="main", queryset=main_queryset)
    stock_formset = BannerImagesFormSet(instance=banner_obj, prefix="stock", queryset=stock_queryset)
    back_formset = BackBannerImagesFormSet(instance=back_banner_obj, prefix="back")


    if request.method == 'POST':
        print("REQUST POST")
        banner_form = BannerForm(request.POST, instance=banner_obj, prefix='banner')
        back_banner_form = BackBannerForm(request.POST, instance=back_banner_obj, prefix='backbanner')

        if "save_main" in request.POST:
            print("SAVE MAIN")
            main_formset = BannerImagesFormSet(request.POST, request.FILES, instance=banner_obj, prefix="main")
            if banner_form.is_valid() and main_formset.is_valid():
                print("VSE VALID")
                saved_banner = banner_form.save()
                work_formset(main_formset, 'main', saved_banner)
                return redirect('banner')


        elif "save_stock" in request.POST:
            print("SAVE STOCK")
            stock_formset = BannerImagesFormSet(request.POST, request.FILES, instance=banner_obj, prefix="stock")
            if banner_form.is_valid() and stock_formset.is_valid():
                print("VSE VALID STOCK")
                saved_banner = banner_form.save()
                work_formset(stock_formset, 'stock', saved_banner)
                return redirect('banner')


        elif "save_back" in request.POST:
            print("SAVE BACK")
            back_formset = BackBannerImagesFormSet(request.POST, request.FILES, instance=back_banner_obj, prefix="back")
            if back_banner_form.is_valid() and back_formset.is_valid():
                print("VSE VALID BACK")
                saved_banner = back_banner_form.save()
                work_formset(back_formset, 'back', saved_banner)

    if request.method == 'GET':
        print("REQUEST GET")
        banner_form = BannerForm(instance=banner_obj, prefix='banner')
        back_banner_form = BackBannerForm(instance=back_banner_obj, prefix='backbanner')
        main_formset = BannerImagesFormSet(instance=banner_obj, prefix="main", queryset=main_queryset)
        stock_formset = BannerImagesFormSet(instance=banner_obj, prefix="stock", queryset=stock_queryset)
        back_formset = BackBannerImagesFormSet(instance=back_banner_obj, prefix="back")

    return render(request, 'banner.html',
                  {'item': banner_obj, 'form': banner_form, 'main_formset': main_formset, 'stock_formset':stock_formset, 'back_formset':back_formset, 'back_form': back_banner_form})
