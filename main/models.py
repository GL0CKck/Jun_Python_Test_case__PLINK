import jwt
from datetime import datetime
from datetime import timedelta
from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):
    def _create_user(self,username,email,password=None,**extra_fields):
        if not username:
            raise ValueError('UserNameValuerError')
        if not email:
            raise ValueError('EmailValueError')

        email=self.normalize_email(email)
        user=self.model(username=username,email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self,username,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)

        return self._create_user(username,email,password,**extra_fields)

    def create_superuser(self,username,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Staff needs True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Staff superuser True')

        return self._create_user(username,email,password,**extra_fields)


class AdvUser(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)

    email = models.EmailField(
        validators=[validators.validate_email],
        unique=True,
        blank=False
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', )
    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username


    def get_short_name(self):
        return self.username


    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%S'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')


class UserIp(models.Model):
    user = models.ForeignKey(AdvUser,on_delete=models.CASCADE,verbose_name='user')
    ip = models.CharField(max_length=100)
    count_post = models.PositiveIntegerField(default=0,verbose_name='POST')
    count_get = models.PositiveIntegerField(default=0,verbose_name='GET')

    def __str__(self):
        return self.ip

    class Meta:
        pass