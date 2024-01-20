# Generated by Django 3.2.13 on 2024-01-09 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wv_app', '0002_auto_20240109_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attraction',
            name='tags',
            field=models.ManyToManyField(blank=True,
                                         related_name='attractions',
                                         to='wv_app.Tag'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='negative_tags',
            field=models.ManyToManyField(blank=True,
                                         related_name='negative_profiles',
                                         to='wv_app.Tag'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='positive_tags',
            field=models.ManyToManyField(blank=True,
                                         related_name='positive_profiles',
                                         to='wv_app.Tag'),
        ),
    ]