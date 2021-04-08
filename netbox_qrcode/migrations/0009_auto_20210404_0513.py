# Generated by Django 3.1.7 on 2021-04-04 05:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dcim', '0122_standardize_name_length'),
        ('netbox_qrcode_ui', '0008_auto_20210404_0454'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qrextendeddevice',
            name='device',
        ),
        migrations.RemoveField(
            model_name='qrextendeddevice',
            name='id',
        ),
        migrations.AddField(
            model_name='qrextendeddevice',
            name='device_ptr',
            field=models.OneToOneField(auto_created=True, default=None, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='dcim.device'),
            preserve_default=False,
        ),
    ]
