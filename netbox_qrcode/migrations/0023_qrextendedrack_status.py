# Generated by Django 3.1.7 on 2021-04-06 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netbox_qrcode_ui', '0022_qrextendeddevice_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='qrextendedrack',
            name='status',
            field=models.CharField(default='active', max_length=50),
        ),
    ]
