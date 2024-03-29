# Generated by Django 2.2.3 on 2019-08-14 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BiodataPeserta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namaDepan', models.CharField(max_length=20)),
                ('namaBelakang', models.CharField(max_length=20)),
                ('jenisKelamin', models.PositiveSmallIntegerField()),
                ('tanggalLahir', models.DateField()),
                ('noKontak', models.CharField(max_length=13)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
