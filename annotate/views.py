from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Annotation, Image, SeriesReview
from .serializers import AnnotationSerializer, ImageSerializer, SeriesReviewSerializer
from .series_utils import series_query_params


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    @action(detail=True, methods=["get", "post"], url_path="annotations")
    def annotations(self, request, pk=None):
        image = self.get_object()
        if request.method == "GET":
            serializer = AnnotationSerializer(image.annotations.all(), many=True)
            return Response(serializer.data)

        serializer = AnnotationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(image=image)
        return Response(serializer.data, status=201)

    @action(detail=True, methods=["delete"], url_path="annotations/clear")
    def clear_annotations(self, request, pk=None):
        image = self.get_object()
        image.annotations.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnnotationViewSet(viewsets.ModelViewSet):
    serializer_class = AnnotationSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "delete"]

    def get_queryset(self):
        return Annotation.objects.filter(image__user=self.request.user).select_related("image")


class ClearSeriesAnnotationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        series_filter = series_query_params(request)
        images = Image.objects.filter(user=request.user, **series_filter)
        Annotation.objects.filter(image__in=images).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SeriesReviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        lookup = series_query_params(request)
        review, _ = SeriesReview.objects.get_or_create(user=request.user, **lookup)
        return Response(SeriesReviewSerializer(review).data)

    def patch(self, request):
        lookup = series_query_params(request)
        review, _ = SeriesReview.objects.get_or_create(user=request.user, **lookup)
        serializer = SeriesReviewSerializer(review, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
