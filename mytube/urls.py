from django.urls import path 
from mytube.views import *

urlpatterns = [
        path('', index.as_view()),
        path('single', single.as_view()),
        path('browse', browse.as_view()),
        path('foo', foo.as_view()),
        path('reload', ureload, name='reload'),
        path('fromfile', video_from_filesystem, name='fromfile'),
        path('fromtor', video_from_torrent, name='fromtor'),
        path('upfiles', update_files, name='updiles'),
    ]
