# Generated by Django 4.0.5 on 2022-06-26 10:19

import app1.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0016_rename_created_date_watchhistory_last_viewed'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='prof_pic',
            field=models.ImageField(blank=True, default=app1.models.get_default_profile_image, null=True, upload_to=''),
        ),
    ]
