# Generated by Django 3.2 on 2021-04-20 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dcim', '0122_standardize_name_length'),
        ('netbox_qrcode', '0002_auto_20210420_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrextendedrack',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='dcim.rackrole'),
        ),
    ]
