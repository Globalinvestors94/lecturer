# Generated by Django 4.2.11 on 2024-08-16 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecture', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scratch_pin',
            name='usage_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
