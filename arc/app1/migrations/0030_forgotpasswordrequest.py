# Generated by Django 4.0.5 on 2022-07-08 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0029_alter_customer_email_alter_file_is_vid'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForgotPasswordRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typedusername', models.CharField(max_length=50)),
            ],
        ),
    ]
