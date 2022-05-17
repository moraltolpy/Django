import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.urls import reverse
from pytils.translit import slugify

class Article(models.Model):
    aut_username = models.TextField("Автордың логины")
    author = models.CharField(verbose_name='Ғылыми жұмыстың авторы', max_length=255)
    title = models.CharField(max_length=255, verbose_name="Ғылыми жұмыстың тақырыбы")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Ғылыми жұмыстың url-адресі",default=uuid.uuid4)
    subject = models.TextField(blank=True, verbose_name="Ғылыми жұмыстың сипаттамасы")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Ғылыми жұмыстың құрылу уақыты")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Ғылыми жұмыстың өзгеру уақыты")
    type = models.ForeignKey('Worktype', on_delete=models.PROTECT, verbose_name="Ғылыми жұмыстың түрлері")
    score = models.DecimalField(max_digits=3,decimal_places=0, verbose_name="Ғылыми жұмыстың бағасы",default='0')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    class Meta:
        verbose_name = 'Ғылыми жұмыс'
        verbose_name_plural = 'Ғылыми жұмыстар'
        ordering = ['-id']

class Worktype(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Ғылыми жұмыстың түрі")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Ғылыми жұмыстың url-адресі")

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('type', kwargs={'type_slug': self.slug})
    class Meta:
        verbose_name = 'Ғылыми жұмыстың түрі'
        verbose_name_plural = 'Ғылыми жұмыстың түрлері'
        ordering = ['id']

class Foreign_Students(models.Model):
    aut_username = models.TextField("Автордың логины")
    author = models.CharField(verbose_name='Ғылыми жұмыстың авторы', max_length=255)
    students = models.DecimalField(max_digits=2,decimal_places=0, verbose_name="Шетел студенттер саны",default='0')
    time_update = models.DateTimeField(auto_now=True, verbose_name="Ғылыми жұмыстың өзгеру уақыты")

    class Meta:
        verbose_name = 'Шетел студенттер'
        verbose_name_plural = 'Шетел студенттер'
        ordering = ['-author']

