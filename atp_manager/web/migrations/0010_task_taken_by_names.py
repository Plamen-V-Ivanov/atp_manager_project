# Generated by Django 3.2.12 on 2022-04-24 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_auto_20220422_0041'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='taken_by_names',
            field=models.TextField(default='None'),
        ),
    ]
