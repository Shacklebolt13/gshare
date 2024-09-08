"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from src.common import views as common_views
from src.video_processor import api as video_api

router = routers.DefaultRouter()
router.register("", video_api.SubtitleViewSet, basename="subtitle")

urlpatterns = [
    path("admin", admin.site.urls),
    # Api endpoints
    path("video", video_api.ListVideoApiView.as_view(), name="video"),
    path("subtitle", include(router.urls)),
    # Views
    path("", common_views.list_videos),
]

urlpatterns.extend(
    static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
)
urlpatterns.extend(
    static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
)

if settings.DEBUG == True:
    from debug_toolbar.toolbar import debug_toolbar_urls  # type: ignore

    urlpatterns.extend(debug_toolbar_urls())
