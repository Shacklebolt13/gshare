from django.shortcuts import get_object_or_404, render
from rest_framework.serializers import Serializer

# Create your views here.


def list_videos(request):
    return render(request, "common/video_list.html")
