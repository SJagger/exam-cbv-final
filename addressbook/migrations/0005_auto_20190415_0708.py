# Generated by Django 2.0.13 on 2019-04-14 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addressbook', '0004_auto_20190411_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addressbooklist',
            name='cnumber',
            field=models.CharField(max_length=12, verbose_name='Contact Number'),
        ),
    ]
