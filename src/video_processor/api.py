from django.apps import apps
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Subtitle, Video


class ListVideoApiView(ListAPIView, CreateAPIView):
    class VideoSerializer(ModelSerializer):
        class Meta:
            model = Video
            fields = ["id", "status", "title", "file", "log_file"]
            kwargs = {
                "id": {"read_only": True},
                "status": {"read_only": True},
                "log_file": {"read_only": True},
            }

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
            language = serializers.CharField()

        serializer = GetSubtitleSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        video_id = serializer.validated_data["video_id"]
        language = serializer.validated_data["language"]
        return Subtitle.objects.filter(video_id=video_id, language=language)

    @action(detail=False, url_name="languages", url_path="languages")
    def get_languages(self, request: Request):
        class ListLanguagesSerializer(Serializer):
            video_id = serializers.UUIDField()

        serializer = ListLanguagesSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        video_id = serializer.validated_data["video_id"]
        language_set = sorted(
            set(
                Subtitle.objects.filter(video_id=video_id).values_list(
                    "language", flat=True
                )
            )
        )
        return Response(language_set, status=200)
