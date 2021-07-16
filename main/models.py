from django.db import models
from django.contrib.auth.models import AbstractUser


class AdvUser(AbstractUser):

    class Meta(AbstractUser.Meta):
        pass


class UserIp(models.Model):
    user = models.ForeignKey(AdvUser,on_delete=models.CASCADE,verbose_name='user')
    ip = models.CharField(max_length=100)
    count_post = models.PositiveIntegerField(default=0,verbose_name='POST')
    count_get = models.PositiveIntegerField(default=0,verbose_name='GET')

    def __str__(self):
        return self.ip

    class Meta:
        pass