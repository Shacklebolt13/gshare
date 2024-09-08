from django.apps import apps
from rest_framework import serializers
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Subtitle, Video

Job = apps.get_model("files", "Job")


class ListVideoApiView(ListAPIView):
    class VideoSerializer(ModelSerializer):
        class JobSerializer(ModelSerializer):
            class Meta:
                model = Job
                fields = ["id", "title", "status", "file"]

        job = JobSerializer()

        class Meta:
            model = Video
            fields = ["job", "id"]

    serializer_class = VideoSerializer
    queryset = Video.objects.all()


class SubtitleViewSet(ReadOnlyModelViewSet):
    class SubtitleSerializer(ModelSerializer):
        class Meta:
            model = Subtitle
            fields = [
                "video",
                "sequence",
                "language",
                "description",
                "start_time",
                "end_time",
            ]

    serializer_class = SubtitleSerializer
    filter_backends = [SearchFilter]
    search_fields = ["description"]
    model = Subtitle

    def get_queryset(self):
        class GetSubtitleSerializer(Serializer):
            video_id = serializers.UUIDField()

        serializer = GetSubtitleSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        video_id = serializer.validated_data["video_id"]
        return Subtitle.objects.filter(video_id=video_id)
