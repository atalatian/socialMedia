# Generated by Django 3.1.7 on 2021-03-18 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialMediaApp', '0018_auto_20210318_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]