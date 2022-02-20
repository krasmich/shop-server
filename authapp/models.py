from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from django.dispatch import receiver
# Create your models here.


def default_key_expiration_date():
    return timezone.now() + timedelta(hours=48)


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_avatars', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст', default=18, null=True)

    activation_key = models.CharField(verbose_name='ключ активации', max_length=128, null=True)
    activation_expiration_date = models.DateTimeField(verbose_name='активация истекает',
                                                      default=default_key_expiration_date)

    def is_activation_key_expired(self):
        return self.activation_expiration_date < timezone.now()


class ShopUserProfile(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    NONBINARY = 'X'

    GENDER_CHOICES = (
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина'),
        (NONBINARY, 'Небинарный'),
    )

    user = models.OneToOneField(ShopUser, null=False, db_index=True, on_delete=models.CASCADE)
    tagline = models.CharField(verbose_name='теги', max_length=256, blank=True)
    about_me = models.TextField(verbose_name='о себе', max_length=512, blank=True)
    gender = models.CharField(verbose_name='гендер', max_length=1, choices=GENDER_CHOICES, blank=True)

    @receiver(post_save, sender=ShopUser)
    def create_or_save_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)
        else:
            instance.shopuserprofile.save()
