from django.contrib import admin
from .models import AdvUser, UserIp, UserNotes
from .forms import RegisterUserForm, UserIpForm, NotesUserForm

# Register your models here.


class UserIpLine(admin.TabularInline):
    model = UserIp


class NotesUserAdmin(admin.ModelAdmin):
    form=NotesUserForm


class AdvUserAdmin(admin.ModelAdmin):
    form = RegisterUserForm
    inlines = (UserIpLine,)


class UserIpAdmin(admin.ModelAdmin):
    form = UserIpForm
    list_filter = ('count_post','count_get')


admin.site.register(AdvUser, AdvUserAdmin)
admin.site.register(UserIp, UserIpAdmin)
admin.site.register(UserNotes,NotesUserAdmin)