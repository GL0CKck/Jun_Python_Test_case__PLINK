from .views import index, registeruserview
from django.urls import path


app_name='main'
urlpatterns = [

    path('',index,name='index'),
    path('register/',registeruserview,name='register'),
]