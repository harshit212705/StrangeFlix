# Generated by Django 3.1.2 on 2020-10-05 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20201002_1102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetails',
            name='wallet_money',
            field=models.IntegerField(default=0),
        ),
    ]
