# Generated by Django 2.2.3 on 2019-08-06 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akun', '0017_delete_tokendefault'),
    ]

    operations = [
        migrations.CreateModel(
            name='Kecamatan',
            fields=[
                ('id_kecamatan', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('f_id_kota', models.SmallIntegerField()),
                ('nama_kecamatan', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'kecamatan',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Kota',
            fields=[
                ('id_kota', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('f_id_prov', models.IntegerField()),
                ('nama_kota', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'kota',
                'managed': False,
            },
        ),
    ]
