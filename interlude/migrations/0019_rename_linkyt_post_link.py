# Generated by Django 4.2.1 on 2023-06-30 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interlude', '0018_comment_userpp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='linkyt',
            new_name='link',
        ),
    ]