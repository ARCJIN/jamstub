# Generated by Django 4.0.5 on 2022-07-02 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0021_tag_topic_ad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='topic',
            field=models.CharField(blank=True, choices=[('Genre', 'Genre'), ('Category', 'Category'), ('Positions', 'Positions'), ('Company', 'Company'), ('Actors', 'Actors'), ('Location', 'Location')], max_length=20),
        ),
    ]
