from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Job, JobStatus


class JobApiView(APIView):

    def get(self, request):
        class GetJobSerializer(serializers.Serializer):
            id = serializers.UUIDField()

        class JobResponseSerializer(serializers.ModelSerializer):
            class Meta:
                model = Job
                fields = ["id", "status", "created_at", "updated_at"]

        serializer = GetJobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        job = get_object_or_404(Job, id=serializer.validated_data["id"])
        return Response(JobResponseSerializer(job).data)

    def post(self, request):
        class CreateJobSerializer(serializers.Serializer):
            file = serializers.FileField()

        class JobResponseSerializer(serializers.ModelSerializer):
            class Meta:
                model = Job
                fields = ["id", "status", "created_at", "updated_at"]

        serializer = CreateJobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        uploadJob = serializer.save()
        return Response(
            JobResponseSerializer(uploadJob).data, status=status.HTTP_201_CREATED
        )
