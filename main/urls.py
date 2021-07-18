from .views import index, registeruserview,  APIView,api_users,api_usersip,ApiAdvUser,UserProfileCreateView,\
    UserProfileDetailView, UserLoginView, profile, UserLogoutView,RegistrApiView,LoginApiView
from django.urls import path, include

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('users',ApiAdvUser)

app_name='main'

urlpatterns = [
    path('api/',include(router.urls)),
    # path('api/users/',api_users),
    # path('api/users/ip/',api_usersip),
    path('registration/',RegistrApiView.as_view(),name='registr_user'),
    path('login/',LoginApiView.as_view(),name='login_user'),
    path('all-profiles/',UserProfileCreateView.as_view()),
    path('profile/<int:pk>/',UserProfileDetailView.as_view()),
    path('', index, name='index'),
    path('register/', registeruserview, name='register'),
    path('accounts/login/',UserLoginView.as_view(),name='login'),
    path('accounts/profile/',profile,name='profile'),
    path('account/logout/',UserLogoutView.as_view(),name='logout'),
]