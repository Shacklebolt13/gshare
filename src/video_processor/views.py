from django.shortcuts import get_object_or_404, render
from rest_framework.serializers import Serializer

from .models import Video

# Create your views here.


def list_videos(request):
    return render(request, "video_processor/video_list.html")


def get_video(request, video_id):
    # get_object_or_404(Video, id=video_id)
    return render(request, "video_processor/video_play.html")
