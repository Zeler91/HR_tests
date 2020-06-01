# Generated by Django 3.0.5 on 2020-06-01 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='completed_tests',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='tests',
            field=models.ManyToManyField(blank=True, to='app.Test'),
        ),
    ]