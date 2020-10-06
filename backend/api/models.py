from django.db import models
from django.contrib.auth.models import AbstractUser


class Product(models.Model):
    title = models.CharField(unique=True, max_length=200,
                             help_text='Product name')
    description = models.TextField(help_text='Product description')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(unique=True, max_length=100,
                             help_text='Category name')

    def __str__(self):
        return self.title


class Company(models.Model):
    name = models.CharField(max_length=100, help_text='Company name')
    description = models.TextField(help_text='Company description')
    customers = models.ManyToManyField('User', blank=True,
                                       related_name='customers')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(unique=True, max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)