# Generated by Django 3.2 on 2021-04-20 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tayf_auth', '0003_alter_customuser_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='is_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
