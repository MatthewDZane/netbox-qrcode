# Generated by Django 3.1.7 on 2021-04-05 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dcim', '0122_standardize_name_length'),
        ('netbox_qrcode_ui', '0020_auto_20210405_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrextendeddevice',
            name='device_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='dcim.devicetype'),
        ),
    ]
