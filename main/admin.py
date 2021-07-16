from django.contrib import admin
from .models import AdvUser, UserIp
from .forms import RegisterUserForm, UserIpForm
# Register your models here.


class UserIpLine(admin.TabularInline):
    model = UserIp


class AdvUserAdmin(admin.ModelAdmin):
    form = RegisterUserForm
    inlines = (UserIpLine,)


class UserIpAdmin(admin.ModelAdmin):
    form = UserIpForm
    list_filter = ('count_post','count_get')


admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(UserIp, UserIpAdmin)