# Generated by Django 2.2.3 on 2019-07-29 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akun', '0012_requestresetpass'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountprofile',
            name='person',
            field=models.CharField(default='default', max_length=30),
            preserve_default=False,
        ),
    ]
