# Generated by Django 3.0.8 on 2020-07-07 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userManager', '0005_remove_myphotos_uploaded_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='myphotos',
            name='uploaded_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
