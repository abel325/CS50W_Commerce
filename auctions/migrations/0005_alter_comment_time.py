# Generated by Django 4.2.7 on 2023-12-05 09:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_alter_comment_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 5, 9, 25, 46, 267336, tzinfo=datetime.timezone.utc)),
        ),
    ]
