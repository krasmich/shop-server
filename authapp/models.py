from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
# Create your models here.


def default_key_expiration_date():
    return timezone.now() + timedelta(hours=48)


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст')

    activation_key = models.CharField(verbose_name='ключ активации', max_length=128, null=True)
    activation_expiration_date = models.DateTimeField(verbose_name='активация истекает',
                                                      default=default_key_expiration_date)

    def is_activation_key_expired(self):
        return self.activation_expiration_date < timezone.now()
