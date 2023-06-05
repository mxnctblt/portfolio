# Generated by Django 4.2.1 on 2023-05-26 16:56

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('interlude', '0002_rename_location_profile_music'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='post_images')),
                ('caption', models.TextField()),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('no_of_likes', models.IntegerField(default=0)),
            ],
        ),
    ]
