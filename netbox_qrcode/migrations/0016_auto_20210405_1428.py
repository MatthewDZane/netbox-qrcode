# Generated by Django 3.1.7 on 2021-04-05 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_qrcode', '0015_auto_20210405_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qrextendedcable',
            name='url',
            field=models.URLField(default=''),
        ),
        migrations.AlterField(
            model_name='qrextendeddevice',
            name='url',
            field=models.URLField(default=''),
        ),
        migrations.AlterField(
            model_name='qrextendedrack',
            name='url',
            field=models.URLField(default=''),
        ),
    ]
