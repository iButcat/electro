# Generated by Django 3.0.6 on 2020-06-04 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0002_group_posts'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='posts',
            new_name='post',
        ),
    ]
