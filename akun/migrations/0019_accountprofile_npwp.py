# Generated by Django 2.2.3 on 2019-08-06 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akun', '0018_kecamatan_kota'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountprofile',
            name='npwp',
            field=models.CharField(blank=True, max_length=23),
        ),
    ]