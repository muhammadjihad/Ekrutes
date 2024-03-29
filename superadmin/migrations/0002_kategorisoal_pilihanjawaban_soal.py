# Generated by Django 2.2.3 on 2019-08-14 07:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='KategoriSoal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('namaKategori', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Soal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pertanyaan', models.TextField()),
                ('timer', models.IntegerField()),
                ('kategori', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='superadmin.KategoriSoal')),
            ],
        ),
        migrations.CreateModel(
            name='PilihanJawaban',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('bobot', models.SmallIntegerField(default=0)),
                ('soal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='superadmin.Soal')),
            ],
        ),
    ]
