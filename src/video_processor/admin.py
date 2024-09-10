from django.contrib import admin

from src.video_processor.models import Subtitle, Video


# Register your models here.
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "status"]
    search_fields = ["title"]
    list_filter = ["status"]


@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ["video", "sequence", "language", "description"]
    search_fields = ["description"]
    list_filter = ["language", "video"]
