from django.db import transaction
from django.db.models import Max
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Tag, Task
from .serializers import TagSerializer, TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user).prefetch_related("tags")
        due_date = self.request.query_params.get("due_date")
        status_filter = self.request.query_params.get("status")
        if due_date:
            queryset = queryset.filter(due_date=due_date)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

    def perform_create(self, serializer):
        status_value = serializer.validated_data.get("status", Task.Status.TODO)
        due_date = serializer.validated_data["due_date"]
        order = serializer.validated_data.get("order")

        if order is None:
            max_order = (
                Task.objects.filter(
                    user=self.request.user,
                    due_date=due_date,
                    status=status_value,
                ).aggregate(max_order=Max("order"))["max_order"]
                or -1
            )
            order = max_order + 1

        serializer.save(user=self.request.user, order=order)

    @action(detail=False, methods=["patch"], url_path="reorder")
    def reorder(self, request):
        updates = request.data.get("tasks", [])
        with transaction.atomic():
            for item in updates:
                Task.objects.filter(id=item["id"], user=request.user).update(
                    status=item["status"], order=item["order"]
                )
        return Response({"ok": True}, status=status.HTTP_200_OK)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
