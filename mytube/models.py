from django.db import models

class Video(models.Model):
    filename = models.CharField(max_length = 100)
    path = models.CharField(max_length = 500)
    download_dir = models.CharField(max_length = 500)
    is_episode = models.BooleanField(default=False)
    episode_num = models.PositiveSmallIntegerField(null=True)
    season = models.PositiveSmallIntegerField(null=True)
    is_finished = models.BooleanField(default=False)
    proper_name = models.CharField(max_length=100)

