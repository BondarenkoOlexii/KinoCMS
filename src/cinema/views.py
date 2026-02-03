from django.shortcuts import render, redirect
from src.cinema.forms import FilmForm, SeoForm, ImageForm, FilmImagesFormSet, CinemaForm, CinemaImagesFormSet, HallForm, HallImagesFormSet
from src.cinema.models import Film, FilmThourghtImage, Cinema, CinemaThourghtImage, Hall, HallThourghtImage
from src.common.models import Image
from src.common.models import SeoBlock
# Create your views here.

def film(request):
    initial_data = [
        {'image_type': 'logo'},
        {'image_type': 'gallery'}
    ]


    if request.method == 'POST':
        form = FilmForm(request.POST, prefix='film')
        seoform = SeoForm(request.POST, prefix='seo')
        image_formset = FilmImagesFormSet(request.POST, request.FILES, prefix='image')  # Імейдж Формсет

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

                return redirect('table_film')

            except Exception as e:
                form.add_error(None, 'Ошибка добавления')
                seoform.add_error(None, 'Ошибка добавления')
        else:
            print(f"Ошибка NewsForm:\n{form.errors.as_text()}")
            print(f"Ошибка SEOForm:\n{seoform.errors.as_text()}")
            print(f"Ошибка ImageFormset:\n {image_formset.errors.as_text()}")
    else:
        form = FilmForm(prefix='film')
        seoform = SeoForm(prefix='seo')
        image_formset = FilmImagesFormSet(initial=initial_data, prefix='image')

        for f in image_formset:
            print(f"Form initial: {f.initial}")

    context = {
        'form': form,
        'seo_form': seoform,
        'image_formset': image_formset,
    }

    return render(request, 'film.html', context)


def table_film(request):
    items = Film.objects.all()
    image_items = FilmThourghtImage.objects.all()
    return render(request, 'table_film.html', {'items': items, 'image_items': image_items})


def delete_film(request, pk):
    delete_item = Film.objects.get(id=pk)
    delete_item_seo = SeoBlock.objects.get(film=delete_item)

    thourd_images = FilmThourghtImage.objects.filter(images_info=delete_item)

    for item in thourd_images:
        Image.objects.filter(id=item.image_id).delete()

    delete_item_seo.delete()
    thourd_images.delete()
    delete_item.delete()

    return redirect('table_film')

def update_film(request, pk):
    item = Film.objects.get(id=pk)
    seo_item = SeoBlock.objects.get(film=item)
    if request.method == 'POST':

        form = FilmForm(request.POST, instance=item, prefix='film')
        seoform = SeoForm(request.POST, instance=seo_item, prefix='seo')
        image_formset = FilmImagesFormSet(request.POST, request.FILES, instance=item, prefix="image")

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

            return redirect('table_film')
    if request.method == 'GET':
        form = FilmForm(instance=item, prefix='film')
        seoform = SeoForm(instance=seo_item, prefix='seo')
        image_formset = FilmImagesFormSet(instance=item, prefix="image")

    return render(request, 'film.html',
                  {'item': item, 'seo_item': seo_item, 'form': form, 'seo_form': seoform,
                   'image_formset': image_formset})


#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------

def cinema(request):
    initial_data = [
        {'image_type': 'logo'},
        {'image_type': 'banner'},
        {'image_type': 'gallery'}
    ]

    if request.method == 'POST':
        cinema_form = CinemaForm(request.POST, prefix='cinema')
        seoform = SeoForm(request.POST, prefix='seo')
        image_formset = CinemaImagesFormSet(request.POST, request.FILES, prefix='image')  # Імейдж Формсет


        if cinema_form.is_valid() and seoform.is_valid() and image_formset.is_valid():
            try:

                seo_instence = seoform.save()  # Зберігаємо seoform в базі данних а seo_instence тепер тримає в собі id цього запису

                cinema_instence = cinema_form.save(commit=False)  # Створюємо об'єкт для збереження, але не закидуємо його в бд

                cinema_instence.seoblock = seo_instence  # Прив'язуємо запис SEOBLOCK до news

                cinema_instence.save()  # А тепер уже зберігаємо news в базі данних

                for form in image_formset:

                    image_obj = form.cleaned_data.get("image")  # Тут беремо нашу фотографію
                    if not image_obj:
                        continue

                    upload_image = Image.objects.create(photo=image_obj)  # Тут суємо її в Таблицю з фоточками

                    thourht_instance = form.instance  # Ось це форма нашої проміжної моделі

                    thourht_instance.image = upload_image  # Ось тут наше посилання на картінку з Image ми сунемо в проміжну таблицю

                    thourht_instance.images_info = cinema_instence  # А це ми сунемо ID тої новини яку раніше зберегли, пов'язучи таблиці між собою

                    thourht_instance.image_type = form.cleaned_data.get('image_type')

                    thourht_instance.save()  # Зберігаємо

                return redirect('table_cinema')

            except Exception as e:
                cinema_form.add_error(None, f'Ошибка добавления {e}')
                seoform.add_error(None, f'Ошибка добавления {e}')
        else:
            print(f"Ошибка NewsForm:\n{cinema_form.errors.as_text()}")
            print(f"Ошибка SEOForm:\n{seoform.errors.as_text()}")
            print(f"Ошибка ImageFormset:\n {image_formset.errors.as_text()}")
    else:
        cinema_form = CinemaForm(prefix='cinema')
        seoform = SeoForm(prefix='seo')
        image_formset = CinemaImagesFormSet(initial=initial_data, prefix='image')

        for f in image_formset:
            print(f"Form initial: {f.initial}")


    context = {
        'form': cinema_form,
        'seo_form': seoform,
        'image_formset': image_formset,
    }

    return render(request, 'cinema.html', context)

def table_cinema(request):
    items = Cinema.objects.all()
    image_items = CinemaThourghtImage.objects.all()
    return render(request, 'table_cinema.html', {'items': items, 'image_items': image_items })

def delete_cinema(request, pk):
    delete_item = Cinema.objects.get(id=pk)
    delete_item_seo = SeoBlock.objects.get(cinema=delete_item)

    thourd_images = CinemaThourghtImage.objects.filter(images_info=delete_item)

    for item in thourd_images:
        Image.objects.filter(id=item.image_id).delete()

    delete_item_seo.delete()
    thourd_images.delete()
    delete_item.delete()

    return redirect('table_cinema')

def update_cinema(request, pk):
    item = Cinema.objects.get(id=pk)
    seo_item = SeoBlock.objects.get(cinema=item)
    if request.method == 'POST':

        form = CinemaForm(request.POST, instance=item, prefix='cinema')
        seoform = SeoForm(request.POST, instance=seo_item, prefix='seo')
        image_formset = CinemaImagesFormSet(request.POST, request.FILES, instance=item, prefix="image")

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

                if not form.has_changed():  # Перевіряємо чи трогав щось користувач в формсеті
                    continue  # Пропускаємо ітерацію якщо нічого не трогав
                image_file = form.cleaned_data.get(
                    'image')  # Якщо, все ж падло щось потрогало то достаємо картінку і тримаємо її

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

            return redirect('update_cinema', pk=pk)
    if request.method == 'GET':
        form = CinemaForm(instance=item, prefix='cinema')
        seoform = SeoForm(instance=seo_item, prefix='seo')
        image_formset = CinemaImagesFormSet(instance=item, prefix="image")
        items = Hall.objects.filter(cinema=pk)

    return render(request, 'cinema.html',
                  {'item': item, 'seo_item': seo_item, 'form': form, 'seo_form': seoform,
                   'image_formset': image_formset, 'items':items})


#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------


# ПОТРІБНО ПРИДУМАТИ ЯК ПЕРЕДАВАТИ CINEMA ID В HALL !!!!!!!!!!!!!!!!!!!!!!!
def hall(request, cinema_id):
    cinema_obj = Cinema.objects.get(id=cinema_id)

    initial_data = [
        {'image_type': 'logo'},
        {'image_type': 'banner'},
        {'image_type': 'gallery'}
    ]

    if request.method == 'POST':
        hall_form = HallForm(request.POST, prefix='hall')
        seoform = SeoForm(request.POST, prefix='seo')
        image_formset = HallImagesFormSet(request.POST, request.FILES, prefix='image')  # Імейдж Формсет

        if hall_form.is_valid() and seoform.is_valid() and image_formset.is_valid():
            try:

                seo_instence = seoform.save()  # Зберігаємо seoform в базі данних а seo_instence тепер тримає в собі id цього запису

                hall_instence = hall_form.save(commit=False)  # Створюємо об'єкт для збереження, але не закидуємо його в бд

                hall_instence.seoblock = seo_instence  # Прив'язуємо запис SEOBLOCK до news

                hall_instence.cinema = cinema_obj

                hall_instence.save()  # А тепер уже зберігаємо news в базі данних
                print("HALL ХОРОШО")

                for form in image_formset:

                    image_obj = form.cleaned_data.get("image")  # Тут беремо нашу фотографію
                    if not image_obj:
                        continue

                    upload_image = Image.objects.create(photo=image_obj)  # Тут суємо її в Таблицю з фоточками

                    thourht_instance = form.instance  # Ось це форма нашої проміжної моделі

                    thourht_instance.image = upload_image  # Ось тут наше посилання на картінку з Image ми сунемо в проміжну таблицю

                    thourht_instance.images_info = hall_instence  # А це ми сунемо ID тої новини яку раніше зберегли, пов'язучи таблиці між собою

                    thourht_instance.image_type = form.cleaned_data.get('image_type')

                    thourht_instance.save()  # Зберігаємо

                return redirect('table_cinema')

            except Exception as e:
                print(e)
                hall_form.add_error(None, f'Ошибка добавления {e}')
                seoform.add_error(None, f'Ошибка добавления {e}')
        else:
            print("HALL ERRORS:", hall_form.errors)
            print("SEO ERRORS:", seoform.errors)
            print("IMAGE FORMSET ERRORS:", image_formset.errors)
            print("IMAGE NON-FORM ERRORS:", image_formset.non_form_errors())
    else:
        hall_form = HallForm(prefix='hall')
        seoform = SeoForm(prefix='seo')
        image_formset = HallImagesFormSet(initial=initial_data, prefix='image')


    context = {
        'hall_form': hall_form,
        'seo_form': seoform,
        'image_formset': image_formset,
        'cinema': cinema_obj,
    }

    return render(request, 'hall.html', context)


def delete_hall(request, pk):
    print("ФУНКЦІЯ СПРАЦЬОВАЛА")
    delete_item = Hall.objects.get(id=pk)
    delete_item_seo = SeoBlock.objects.get(hall=delete_item)
    cinema_id = delete_item.cinema.id

    thourd_images = HallThourghtImage.objects.filter(images_info=delete_item)

    for item in thourd_images:
        Image.objects.filter(id=item.image_id).delete()

    delete_item_seo.delete()
    thourd_images.delete()
    delete_item.delete()

    return redirect('delete_cinema', pk=cinema_id)

def update_hall(request,cinema_pk, hall_pk):
    print("ФУНКЦІЯ СПРАЦЬОВАЛА")
    item = Hall.objects.get(id=hall_pk)
    seo_item = SeoBlock.objects.get(hall=item)
    cinema_id = item.cinema.id
    if request.method == 'POST':

        form = HallForm(request.POST, instance=item, prefix='hall')
        seoform = SeoForm(request.POST, instance=seo_item, prefix='seo')
        image_formset = HallImagesFormSet(request.POST, request.FILES, instance=item, prefix="image")

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

                if not form.has_changed():  # Перевіряємо чи трогав щось користувач в формсеті
                    continue  # Пропускаємо ітерацію якщо нічого не трогав
                image_file = form.cleaned_data.get(
                    'image')  # Якщо, все ж падло щось потрогало то достаємо картінку і тримаємо її

                if image_file:  # Перевіряємо чи картінка не пуста

                    if not form.instance.image_id:  # Якщо вона не пуста і користувач ДОДАВ картинку
                        update_image = Image.objects.create(
                            photo=image_file)  # Записуємо цю картинку в Image і тримаємо її id

                    else:  # Якщо оказалось що він просто змінив стару картінку
                        form.instance.image.photo = image_file  # Міняємо картінку  на нову

                        form.instance.image.save()  # Зберігаємо цю картінку

                        update_image = form.instance.image

                    thourgh_form = form.instance

                    thourgh_form.image = update_image

                    thourgh_form.image_info = form_instance

                    thourgh_form.save()

            return redirect('update_cinema', pk=cinema_id)
    else:
        form = HallForm(instance=item, prefix='hall')
        seoform = SeoForm(instance=seo_item, prefix='seo')
        image_formset = HallImagesFormSet(instance=item, prefix="image")

    return render(request, 'hall.html',
                  {'item': item, 'seo_item': seo_item, 'hall_form': form, 'seo_form': seoform,
                   'image_formset': image_formset})