# Generated by Django 3.2.12 on 2022-05-12 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='foreign_students',
            name='time_update',
            field=models.DateTimeField(auto_now=True, verbose_name='Ғылыми жұмыстың өзгеру уақыты'),
        ),
    ]