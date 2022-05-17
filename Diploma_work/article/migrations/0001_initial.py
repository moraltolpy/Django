# Generated by Django 3.2.12 on 2022-05-10 04:03

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Foreign_Students',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aut_username', models.TextField(verbose_name='Автордың логины')),
                ('author', models.CharField(max_length=255, verbose_name='Ғылыми жұмыстың авторы')),
                ('students', models.CharField(default='0', max_length=3, verbose_name='Шетел студенттер саны')),
            ],
            options={
                'verbose_name': 'Шетел студенттер',
                'verbose_name_plural': 'Шетел студенттер',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Worktype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name='Ғылыми жұмыстың түрі')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Ғылыми жұмыстың url-адресі')),
            ],
            options={
                'verbose_name': 'Ғылыми жұмыстың түрі',
                'verbose_name_plural': 'Ғылыми жұмыстың түрлері',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aut_username', models.TextField(verbose_name='Автордың логины')),
                ('author', models.CharField(max_length=255, verbose_name='Ғылыми жұмыстың авторы')),
                ('title', models.CharField(max_length=255, verbose_name='Ғылыми жұмыстың тақырыбы')),
                ('slug', models.SlugField(default=uuid.uuid4, max_length=255, unique=True, verbose_name='Ғылыми жұмыстың url-адресі')),
                ('subject', models.TextField(blank=True, verbose_name='Ғылыми жұмыстың сипаттамасы')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Ғылыми жұмыстың құрылу уақыты')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Ғылыми жұмыстың өзгеру уақыты')),
                ('score', models.CharField(default='0', max_length=3, verbose_name='Ғылыми жұмыстың бағасы')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='article.worktype', verbose_name='Ғылыми жұмыстың түрлері')),
            ],
            options={
                'verbose_name': 'Ғылыми жұмыс',
                'verbose_name_plural': 'Ғылыми жұмыстар',
                'ordering': ['-id'],
            },
        ),
    ]
