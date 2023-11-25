# Generated by Django 4.2.2 on 2023-11-25 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_user_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(default='', max_length=300, verbose_name='full name'),
            preserve_default=False,
        ),
    ]
