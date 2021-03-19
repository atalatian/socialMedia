# Generated by Django 3.1.7 on 2021-03-18 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialMediaApp', '0017_auto_20210318_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='firstName',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='lastName',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='website',
            field=models.URLField(null=True),
        ),
    ]
