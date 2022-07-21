# Generated by Django 4.0.5 on 2022-06-22 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=100, null=True)),
                ('security_key', models.CharField(max_length=100, null=True)),
                ('desc', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.CharField(blank=True, max_length=200, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='created_date')),
                ('is_blocked', models.BooleanField(default=False, null=True)),
                ('is_login', models.BooleanField(default=False, null=True)),
                ('is_editor', models.BooleanField(default=False, null=True)),
                ('is_invited', models.BooleanField(default=False, null=True)),
                ('gender', models.CharField(blank=True, choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], max_length=20)),
                ('interested', models.CharField(blank=True, choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE'), ('BOTH', 'BOTH')], max_length=20)),
                ('invited_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitor', to='app1.customer')),
            ],
        ),
    ]
