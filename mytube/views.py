from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, FormView
from mytube.models import Video
from django.db.models import Q
import json, re

try:
    import uwsgi
except ModuleNotFoundError: #Not running under uwsgi
    pass

def ureload(request):
    uwsgi.reload()
    return HttpResponse(json.dumps({"Status":"OK"}))

def index(request):
    return HttpResponse("OK")

@csrf_exempt
def video_from_filesystem(request):
    data = json.loads(request.body.decode("utf-8"))
    videos = []
    for f in data:
        if Video.objects.filter(filename=f["filename"]): continue
        videos.append(Video (
            filename = f["filename"],
            path = f["path"],
            download_dir = f["download_dir"],
            is_episode = f["is_episode"],
            episode_num = f["episode_num"],
            season = f["season"],
            proper_name = f["proper_name"],
            is_finished = True,
            ))
    Video.objects.bulk_create(videos)
    return HttpResponse(json.dumps({"status": "OK"}))

@csrf_exempt
def video_from_torrent(request):
    data = json.loads(request.body.decode("utf-8"))
    videos = []
    for f in data["files"]:
        if Video.objects.filter(filename=f["filename"]): continue
        videos.append(Video (
                    filename = f["filename"],
                    path = f["path"],
                    download_dir = data["download_dir"],
                    is_episode = f["is_episode"],
                    episode_num = f["episode_num"],
                    season = f["season"],
                    proper_name = f["proper_name"],
                    is_finished = False,
                    ))
    Video.objects.bulk_create(videos)
    return HttpResponse(json.dumps({"status": "OK"}))

@csrf_exempt
def update_files(request):
    data = json.loads(request.body.decode("utf-8"))
    records = []
    for row in data:
        r = Video.objects.get(filename=row["filename"],path=row["path"])
        r.is_finished = True
        records.append(r)
    Video.objects.bulk_update(records, ["is_finished"])
    return HttpResponse(json.dumps({"status":"OK"}))
# Create your views here.
class foo(TemplateView):
    template_name = "foo.html"


    def bar(self, *args, **kwargs):
        with open("/tmp/aa.json", "w") as f: f.write(json.dumps(self.request.GET))
#        with open("/tmp/debuga.json", "w") as f: f.write(json.dumps(args))
#        with open("/tmp/debug.json", "w") as f: f.write(json.dumps(kwargs))
        return [{"item":"myarg"}]

class index(TemplateView):
    template_name="index.html"

class browse(TemplateView):
    template_name="browse.html"

    def browseitems(self):
        fields = Video.objects.order_by().values("proper_name").distinct()

        data = { x["proper_name"]: [] for x in fields}

        for record in Video.objects.all():
            data[record.proper_name].append({"link": record.id, "season": record.season, "episode_num": record.episode_num})

        return  [{"title":k, "files": v} for k,v in data.items()]


class single(TemplateView):
    template_name="single.html"

    def __init__(self):
        self.downloads_url = "downloads"


    def getsearchterm(self):
        searchterm = self.request.GET.get("search")
        if not searchterm: return (None, None, None)
        try:
            season, episode_num = re.search("(\d+)-(\d+)", searchterm).groups()
        except AttributeError:
            return (searchterm, None, None)
        return (searchterm.replace(season + "-" + episode_num, "").strip(), season, episode_num)


    def mainvideo(self):
        video = {}
        title = ""
        searchterm, season, episode_num = self.getsearchterm()
        if searchterm:
            if season:
                searchterm = searchterm.replace(season + "-" + episode_num, "").strip()
                video = Video.objects.filter(Q(is_finished=True), Q(season=season), Q(episode_num=episode_num),
                        Q(proper_name__icontains=searchterm)| Q(filename__icontains=searchterm) | Q(path__icontains=searchterm)).order_by("season","episode_num").first()
            else:
                video = Video.objects.filter(Q(is_finished=True), Q(proper_name__icontains=searchterm)| Q(filename__icontains=searchterm) | Q(path__icontains=searchterm)).order_by("season", "episode_num").first()
            if not video:
                title = "No Search Results for %s" %(searchterm)
        if self.request.GET.get("link"):
            try:
                video =  Video.objects.get(id=self.request.GET.get("link"))
            except Video.DoesNotExist:
                title = "Invalid video ID"
        if not video:
            video = Video.objects.filter(is_finished=True).order_by("-id").first()
        if not title:
            title = video.proper_name
            if video.season: title += " Season: %d Episode: %d" %(video.season, video.episode_num)
        self.title = title
        return {"target":"/%s/%s/%s"%(self.downloads_url,video.path, video.filename),"title": title}

    def playlist(self):
        searchterm, season, episode_num = self.getsearchterm()
        videos = []
        if searchterm:
            videos = Video.objects.filter(Q(is_finished=True), Q(proper_name__icontains=searchterm)| Q(filename__icontains=searchterm) | Q(path__icontains=searchterm)).order_by("-season", "-episode_num")[:10]

        searches = [{"link": x.id, "title": x.proper_name, "season": x.season, "episode_num": x.episode_num} for x in videos]
        videos = Video.objects.filter(is_finished=True).order_by("-id")[:10 - len(searches)]

        searches += [{"link": x.id, "title": x.proper_name, "season": x.season, "episode_num": x.episode_num} for x in videos]

        return searches

