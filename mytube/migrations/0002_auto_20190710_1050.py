# Generated by Django 2.2.3 on 2019-07-10 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytube', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='torrent',
            name='transmission_id',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='torrent_file',
            field=models.IntegerField(null=True),
        ),
    ]
