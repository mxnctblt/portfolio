# Generated by Django 4.2.1 on 2023-05-29 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interlude', '0005_likepost_alter_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowersCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
            ],
        ),
    ]
