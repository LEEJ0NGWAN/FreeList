# Generated by Django 3.1 on 2020-08-25 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0008_auto_20200824_1344'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='color',
            field=models.CharField(default='#dddddd', max_length=8),
        ),
        migrations.AddField(
            model_name='node',
            name='font',
            field=models.CharField(default='14', max_length=20),
        ),
        migrations.AddField(
            model_name='node',
            name='shape',
            field=models.CharField(default='ellipse', max_length=20),
        ),
    ]
