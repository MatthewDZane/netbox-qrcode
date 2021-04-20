# Generated by Django 3.2 on 2021-04-20 18:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dcim', '0122_standardize_name_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='QRExtendedRack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('photo', models.ImageField(upload_to='image-attachments/')),
                ('url', models.URLField(default='')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(default='active', max_length=50)),
                ('rack', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dcim.rack')),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='+', to='dcim.rackrole')),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='dcim.site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QRExtendedDevice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('photo', models.ImageField(upload_to='image-attachments/')),
                ('url', models.URLField(default='')),
                ('name', models.CharField(blank=True, max_length=64, null=True)),
                ('status', models.CharField(default='active', max_length=50)),
                ('device', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dcim.device')),
                ('device_role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='dcim.devicerole')),
                ('device_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='dcim.devicetype')),
                ('rack', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='dcim.rack')),
                ('site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='dcim.site')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='QRExtendedCable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('photo', models.ImageField(upload_to='image-attachments/')),
                ('url', models.URLField(default='')),
                ('cable', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dcim.cable')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
