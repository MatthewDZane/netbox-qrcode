# Generated by Django 3.1.7 on 2021-04-08 00:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dcim', '0122_standardize_name_length'),
        ('netbox_qrcode_ui', '0024_auto_20210408_0035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrextendeddevice',
            name='device',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dcim.device'),
        ),
    ]
