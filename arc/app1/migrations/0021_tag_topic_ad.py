# Generated by Django 4.0.5 on 2022-07-02 16:48

import app1.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0020_file_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='topic',
            field=models.CharField(blank=True, choices=[('Genre', 'Genre'), ('Category', 'Category'), ('Positions', 'Positions'), ('Company', 'Company'), ('Actors', 'Actors')], max_length=20),
        ),
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('desc', models.CharField(max_length=500)),
                ('content', models.ImageField(blank=True, default=app1.models.get_default_profile_image, null=True, upload_to='')),
                ('is_block', models.BooleanField(default=False, null=True)),
                ('is_special', models.BooleanField(default=False, null=True)),
                ('is_promoted', models.BooleanField(default=False, null=True)),
                ('is_highdemand', models.BooleanField(default=False, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('duration', models.PositiveIntegerField(blank=True, default=7, null=True)),
                ('maker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.customer')),
            ],
        ),
    ]
