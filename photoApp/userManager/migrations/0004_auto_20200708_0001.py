# Generated by Django 3.0.8 on 2020-07-07 18:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('userManager', '0003_auto_20200707_2344'),
    ]

    operations = [
        migrations.CreateModel(
            name='MYPhotos',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('uploaded_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='images/')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Photos',
        ),
    ]
