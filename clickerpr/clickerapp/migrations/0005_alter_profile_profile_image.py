# Generated by Django 5.1.6 on 2025-05-02 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clickerapp', '0004_profile_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
