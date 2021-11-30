from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework.exceptions import ValidationError
from .manager import UserManager
from datetime import date


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('moderator', 'Moderator'),
        ('admin', 'Admin')
    )

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    bio = models.CharField(max_length=100, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=3)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


def validate_date(value):
    current_year = int(date.today().year)
    if value > current_year or value <= 0:
        raise ValidationError('Wrong date!')


class Category(models.Model):
    name = models.TextField('Название категории', blank=False, max_length=150)
    slug = models.SlugField('slug', blank=False, unique=True, db_index=True)

    def __str__(self):
        return self.name[0:10]


class Genre(models.Model):
    name = models.TextField('Название жанра', blank=False, max_length=150)
    slug = models.SlugField('slug', blank=False, unique=True, db_index=True)

    def __str__(self):
        return self.name[0:10]


class Title(models.Model):
    name = models.TextField(
        'Название тайтла',
        blank=False,
        max_length=200,
        db_index=True
    )
    year = models.IntegerField('Год', blank=True, validators=[validate_date])
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='категория'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        db_index=True,
        related_name='titles',
        verbose_name='жанр'
    )
    description = models.CharField(
        'описание',
        max_length=200,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name[0:10]
