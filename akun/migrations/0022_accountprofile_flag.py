# Generated by Django 2.2.3 on 2019-08-12 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akun', '0021_auto_20190806_1314'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountprofile',
            name='flag',
            field=models.BooleanField(default=True),
        ),
    ]
