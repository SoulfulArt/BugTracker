# Generated by Django 3.1.7 on 2021-06-18 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Models_MVC', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_birth',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_photo',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
