# Generated by Django 4.0.5 on 2022-06-22 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_remove_customer_invited_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='invited_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='invitor', to='app1.customer'),
        ),
    ]