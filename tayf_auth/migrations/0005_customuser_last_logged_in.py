# Generated by Django 3.2 on 2021-04-20 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tayf_auth', '0004_customuser_is_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='last_logged_in',
            field=models.DateTimeField(auto_now=True),
        ),
    ]