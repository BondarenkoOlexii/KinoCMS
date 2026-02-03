import os.path

from celery.result import AsyncResult
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from config import settings
from src.user.models import User
from src.user.forms import UserForm, CustomChangePassword, NewsletterForm, User_Choise
from config_celery.worker_cel import send_mail_task, app

# Create your views here.
def user(request):
    if request.method == 'POST':
        form = UserForm(request.POST, prefix='userform')
        password_form = None
        if form.is_valid():
            new_user = form.save(commit=False)
            password_form = CustomChangePassword(user=new_user, data=request.POST, prefix='password_form')
            if password_form.is_valid():
                password_form.save()
                return redirect('table_user')
            else:
                print(f"Ошибка PasswordForm:\n{password_form.errors.as_text()}")
        else:
            print(f"Ошибка UserForm:\n{form.errors.as_text()}")
    else:
        form = UserForm(prefix='userform')
        password_form = CustomChangePassword(user=None, prefix='password_form')

    return render(request, 'admin_users.html', {'form': form, 'password_form': password_form})

def table_user(request):
    items = User.objects.all()
    return render(request, 'table_user.html', {'items': items})

def delete_user(request, pk):
    delete_item = get_object_or_404(User,id=pk)
    delete_item.delete()
    return redirect('table_user.html')

def update_user(request, pk):
    password_form = None
    item = get_object_or_404(User,id=pk)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=item, prefix='userform')
        password_form = CustomChangePassword(user=item, data=request.POST, prefix='password_form')
        if form.is_valid() and password_form.is_valid():
            form.save()
            password_form.save()
        else:
            print(f"Ошибка UserForm:\n{form.errors.as_text()}")
    else:
        form = UserForm(instance=item,prefix='userform')
        password_form = CustomChangePassword(user=item, prefix='password_form')

    return render(request, 'admin_users.html', {'item': item, 'form':form, 'password_form': password_form})

#----------------------------------------------------------------------------------------------------------------------

def distribution(request):
    task_id = None
    if request.method == 'POST':
        form = NewsletterForm(request.POST, request.FILES, prefix='distribution')

        if form.is_valid():
            pdf_file = form.cleaned_data.get('html_email')

            if pdf_file:
                fs = FileSystemStorage()
                file_path = fs.save(pdf_file.name, pdf_file)
                file_url = fs.path(file_path)

                receipte_type = form.cleaned_data['type']


                if receipte_type == 'all':
                    receipte_type = list(User.objects.values_list('email', flat=True))
                    print(receipte_type)
                else:
                    users_ids = request.sessions.get('selected_ids', [])
                    receipte_type = list(User.objects.filter(id__in=users_ids).values_list('email', flat=True))
                    print(receipte_type)

                task = send_mail_task.delay('ABC', 'message', 'mayoright01@gmail.com', receipte_type, file_url)
                task_id = task.id
        else:
            print(form.errors)
    else:
        form = NewsletterForm(prefix='distribution')

    final_list = view_last_files()
    return render(request, 'distribution.html', {'form': form, 'files':final_list, 'task_id': task_id})
    # send_mail_task.delay('ABC', 'ABC', 'ім'я з якого йде email', [] )


def progress_view(request, task_id):
    res = AsyncResult(task_id, app=app)
    print(res.result, res.state)
    return JsonResponse({
        "state": res.state,
        "result": res.result
    })

def view_last_files():
    fs = FileSystemStorage()
    media_path = settings.MEDIA_ROOT

    files = []

    if os.path.exists(media_path):
        for filename in os.listdir(media_path):
            full_path = os.path.join(media_path, filename)
            if os.path.isfile(full_path):
                mtime = os.path.getatime(full_path)
                files.append({
                    'name': filename,
                    'time': mtime,
                    'url': fs.url(filename)
                })

    final_list = sorted(files, key=lambda x: x['time'], reverse=True)[:5]
    return final_list


def delete_file(request, filename):
    fs = FileSystemStorage()
    if fs.exists(filename):
        fs.delete(filename)
    return redirect('distribution')
def choise_users(request):
    if request.method == "POST":

        selected_ids = request.POST.getlist('users_choise-users')

        if selected_ids:
            request.session['selected_ids'] = selected_ids
            return redirect('distribution')
    else:
        usersform = User_Choise(prefix='users_choise')
        users = User.objects.all()

    return render(request, 'choise_users.html', {'form':usersform, 'users':users})