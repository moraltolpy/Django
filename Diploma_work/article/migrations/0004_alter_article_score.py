# Generated by Django 3.2.12 on 2022-05-13 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20220513_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='score',
            field=models.DecimalField(decimal_places=0, default='0', max_digits=3, verbose_name='Ғылыми жұмыстың бағасы'),
        ),
    ]
