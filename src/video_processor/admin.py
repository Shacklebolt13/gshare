from django.contrib import admin

from src.video_processor.models import Subtitle, Video

# Register your models here.
admin.site.register(Video)
admin.site.register(Subtitle)
