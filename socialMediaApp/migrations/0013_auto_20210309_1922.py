# Generated by Django 3.1.7 on 2021-03-09 19:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialMediaApp', '0012_auto_20210309_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='likeUser', to='socialMediaApp.user'),
        ),
    ]