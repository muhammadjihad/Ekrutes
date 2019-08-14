# Generated by Django 2.2.3 on 2019-08-01 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akun', '0013_accountprofile_person'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountstatus',
            name='kategori',
        ),
        migrations.AddField(
            model_name='accountprofile',
            name='jenisAkun',
            field=models.SmallIntegerField(choices=[(0, 'Demo'), (1, 'Premium')], default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='accountprofile',
            name='kategori',
            field=models.CharField(default=2, max_length=1),
        ),
        migrations.AddField(
            model_name='accountprofile',
            name='tokenTest',
            field=models.IntegerField(default=50),
        ),
    ]