from django.shortcuts import render, get_object_or_404, redirect
from src.user.models import User
from src.user.forms import UserForm, CustomChangePassword
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