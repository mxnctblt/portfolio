# Generated by Django 4.2.1 on 2023-06-12 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interlude', '0010_remove_post_userimg'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
        migrations.AddField(
            model_name='post',
            name='linkyt',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
    ]