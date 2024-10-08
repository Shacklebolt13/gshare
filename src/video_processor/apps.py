from django.apps import AppConfig


class VideoProcessorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.video_processor"

    def ready(self):
        import src.video_processor.signals
