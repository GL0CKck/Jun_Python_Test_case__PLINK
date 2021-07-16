from django.shortcuts import render, redirect
from .forms import RegisterUserForm
from django.contrib import messages
from .models import UserIp, AdvUser


def index(request):
    if request.method == 'GET' and request.user.is_authenticated:
        user = request.user
        ip=get_client_ip(request)
        ipuser,c = UserIp.objects.get_or_create(
            user=request.user,
            defaults={
                'ip': ip
            }
        )
        ipuser.count_get += 1
        ipuser.save()
    return render(request, 'index.html',)


def registeruserview(request):
    if request.method == 'POST':
        form=RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('main:index')
    else:
        form=RegisterUserForm()
        context={'form':form}

    messages.add_message(request, messages.WARNING, 'Почта gmail.com и icloud.com не принимается')
    return render(request,'register.html',context)




def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

