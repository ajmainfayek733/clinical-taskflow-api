from PIL import Image as PILImage
from rest_framework import serializers

from .models import Annotation, Image, SeriesReview


class ImageSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = [
            "id",
            "file",
            "file_url",
            "original_name",
            "patient_id",
            "patient_code",
            "test_code",
            "width",
            "height",
            "notes",
            "uploaded_at",
        ]
        read_only_fields = ["width", "height", "uploaded_at", "original_name"]

    def get_file_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return obj.file.url
        return request.build_absolute_uri(obj.file.url)

    def create(self, validated_data):
        file = validated_data["file"]
        width, height = 0, 0

        file.seek(0)
        with PILImage.open(file) as img:
            width, height = img.size
        file.seek(0)

        return Image.objects.create(
            user=self.context["request"].user,
            file=file,
            original_name=file.name,
            patient_id=validated_data.get("patient_id", ""),
            patient_code=validated_data.get("patient_code", ""),
            test_code=validated_data.get("test_code", ""),
            width=width,
            height=height,
        )


class AnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Annotation
        fields = ["id", "image", "label", "color", "points", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at", "image"]

    def validate_points(self, points):
        if not isinstance(points, list) or len(points) < 3:
            raise serializers.ValidationError("A polygon must contain at least 3 points.")
        for point in points:
            if not isinstance(point, list) or len(point) != 2:
                raise serializers.ValidationError("Each point must be [x, y].")
            x, y = float(point[0]), float(point[1])
            if x < 0 or x > 1 or y < 0 or y > 1:
                raise serializers.ValidationError("Point coordinates must be normalized between 0 and 1.")
        return points


class SeriesReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeriesReview
        fields = [
            "patient_id",
            "patient_code",
            "test_code",
            "notes",
            "updated_at",
        ]
        read_only_fields = ["patient_id", "patient_code", "test_code", "updated_at"]
