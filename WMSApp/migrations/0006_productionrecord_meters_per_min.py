# Generated by Django 5.0.14 on 2025-05-28 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WMSApp', '0005_remove_productionrecord_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productionrecord',
            name='meters_per_min',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
    ]
