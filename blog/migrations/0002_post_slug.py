# Generated by Django 3.1.2 on 2020-12-25 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.CharField(default='', max_length=150),
            preserve_default=False,
        ),
    ]
