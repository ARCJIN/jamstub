# Generated by Django 4.0.5 on 2022-07-07 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0026_customer_is_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitecode',
            name='is_restricted',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
