# Generated by Django 3.2.20 on 2023-08-31 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.URLField()),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('ingredients', models.JSONField(blank=True, default=list)),
                ('instructions', models.TextField(blank=True)),
                ('cooking_time', models.PositiveIntegerField()),
                ('servings', models.PositiveIntegerField()),
                ('diet_preference', models.CharField(default='vegan', max_length=50)),
            ],
        ),
    ]
