# Generated by Django 2.2.24 on 2021-08-09 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_registrationconfiguration_reply_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='county',
            field=models.CharField(blank=True, max_length=50, verbose_name='county'),
        ),
    ]
