from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager
from general.models import Organization


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(('email address'), unique=True)
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    phone = models.CharField(max_length=50, verbose_name='Телефон')
    photo = models.ImageField(blank=True, null=True, upload_to='photo_users/', verbose_name='Фото')
    organization = models.ManyToManyField(Organization, related_name='user_organization', verbose_name='Организации')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()

    def __repr__(self) -> str:
        return f'{self.id}'

    def __str__(self):
        return self.email