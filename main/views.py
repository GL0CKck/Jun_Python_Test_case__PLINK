from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from .forms import RegisterUserForm, NotesUserForm
from django.contrib import messages
from .models import UserIp, AdvUser, UserNotes
from .serializers import AdvUserSerializer, AdvUserIpSerializer, RegisterUserSerializer,LoginUserSerializer
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from .license import IsOwnerProfileOrReadOnly
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404


def index(request):
    """ Запрос просто возращает главную страницу сохраняет ip-user и считает сколько запросов было сделано"""
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
    """ ендпоинт регистрации юзера c JWT token через фронт и сохранение его в БД"""
    if request.method == 'POST':
        form=RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect('main:index')
    else:
        form=RegisterUserForm()
        context={'form':form}

    return render(request,'register.html',context)


def get_client_ip(request):
    """ Получаем ip-user """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@api_view(['GET','POST','DELETE'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def api_users(request):
    """ endpoint serializer выдает инф. о юзере в методе GET , в методе POST можем добавить нового юзера,
     в методе DELETE удалить"""
    users = AdvUser.objects.all()
    if request.method=='GET':
        serializer=AdvUserSerializer(users,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer=AdvUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        users.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes((IsAuthenticatedOrReadOnly,))
def api_usersip(request):
    """ endpoint UserIp and count methods"""
    if request.method=='GET':
        users=UserIp.objects.all()
        serializer=AdvUserIpSerializer(users,many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer=AdvUserIpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiAdvUser(ModelViewSet):
    """ """
    queryset = AdvUser.objects.all()
    serializer_class = AdvUserSerializer


class UserLoginView(LoginView):
    """ endpoint logging on web-site """
    template_name = 'login.html'


@login_required
def profile(request):
    """ endpoint profile-user """
    notes=UserNotes.objects.filter(author=request.user.pk)
    context={'notes':notes}
    return render(request,'profile.html',context)

@login_required()
def notes_detail(request,pk):
    notes = get_object_or_404(UserNotes,pk=pk)
    context={'notes':notes}
    return render(request,'notes_detail.html',context)


@login_required()
def notes_add(request):
    if request.method == 'POST':
        form=NotesUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main:profile')
    else:
        form=NotesUserForm(initial={'author':request.user.pk})
    context={'form':form}
    return render(request,'notes_add.html',context)


@login_required()
def notes_change(request,pk):

    notes=get_object_or_404(UserNotes,pk=pk)
    if request.method == 'POST':
        form = NotesUserForm(request.POST,instance=notes)
        if form.is_valid():
            notes=form.save()
            messages.add_message(request, messages.SUCCESS, 'Успешно Изменено')
        return redirect('main:profile')
    else:
        form=NotesUserForm(instance=notes)
    context={'form':form}
    return render(request,'notes_change.html',context)


@login_required()
def notes_delete(request,pk):
    notes=get_object_or_404(UserNotes,pk=pk)
    if request.method == 'POST':
        notes.delete()
        messages.add_message(request,messages.SUCCESS,'Успешно удаленно')
    else:
        context = {'notes':notes}
        return render(request,'notes_delete.html',context)


class UserLogoutView(LoginRequiredMixin,LogoutView):
    """endpoint logout user"""
    template_name = 'logout.html'


class UserProfileCreateView(ListCreateAPIView):
    queryset = AdvUser.objects.all()
    serializer_class = AdvUserSerializer
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(user=user)


class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset = AdvUser.objects.all()
    serializer_class = AdvUserSerializer
    permission_classes=[IsOwnerProfileOrReadOnly,IsAuthenticated]


class RegistrApiView(APIView):
    """ endpoint регистрация с токеном"""
    permission_classes=[AllowAny]
    serializer_class = RegisterUserSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'token':serializer.data.get('token',None),

        },status=status.HTTP_201_CREATED,)


class LoginApiView(APIView):
    """endpoint вход с токеном """
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializer

    def post(self,requests):
        serializer=self.serializer_class(data=requests.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
