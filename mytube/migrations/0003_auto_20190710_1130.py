# Generated by Django 2.2.3 on 2019-07-10 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytube', '0002_auto_20190710_1050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='torrent',
        ),
        migrations.RemoveField(
            model_name='video',
            name='torrent_file',
        ),
        migrations.AddField(
            model_name='video',
            name='is_finished',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='video',
            name='proper_name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Torrent',
        ),
    ]
