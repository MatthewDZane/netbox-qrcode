# Generated by Django 3.1.7 on 2021-04-04 00:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dcim', '0122_standardize_name_length'),
        ('netbox_qrcode', '0003_auto_20210403_2225'),
    ]

    operations = [
        migrations.CreateModel(
            name='QRExtendedCable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('photo', models.ImageField(upload_to=None)),
                ('cable', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dcim.cable')),
            ],
        ),
        migrations.CreateModel(
            name='QRExtendedDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('photo', models.ImageField(upload_to=None)),
                ('device', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dcim.device')),
            ],
        ),
        migrations.CreateModel(
            name='QRExtendedRack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('photo', models.ImageField(upload_to=None)),
                ('rack', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dcim.rack')),
            ],
        ),
        migrations.DeleteModel(
            name='NetboxObject',
        ),
    ]
