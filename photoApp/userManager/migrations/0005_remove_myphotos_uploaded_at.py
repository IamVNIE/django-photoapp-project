# Generated by Django 3.0.8 on 2020-07-07 18:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userManager', '0004_auto_20200708_0001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myphotos',
            name='uploaded_at',
        ),
    ]
