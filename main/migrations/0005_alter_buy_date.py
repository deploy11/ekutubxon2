# Generated by Django 5.0.1 on 2024-04-18 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy',
            name='date',
            field=models.DateField(verbose_name='Kitob Berilgan Muddat'),
        ),
    ]
