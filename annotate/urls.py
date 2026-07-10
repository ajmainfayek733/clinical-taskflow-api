from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import AnnotationViewSet, ClearSeriesAnnotationsView, ImageViewSet, SeriesReviewView

router = DefaultRouter()
router.register(r"images", ImageViewSet, basename="image")
router.register(r"annotations", AnnotationViewSet, basename="annotation")

urlpatterns = [
    path("series-review/", SeriesReviewView.as_view(), name="series-review"),
    path(
        "series-annotations/clear/",
        ClearSeriesAnnotationsView.as_view(),
        name="series-annotations-clear",
    ),
    *router.urls,
]
