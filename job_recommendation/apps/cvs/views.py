
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import CVUploadSerializer
from .models import CV
from .tasks import process_cv


class CVUploadView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):
        serializer = CVUploadSerializer(data=request.data)
        if serializer.is_valid():
            cv = serializer.save(owner=request.user)
            # queue background processing
            process_cv.delay(cv.id)
            return Response({'id': cv.id, 'message': 'uploaded, processing started'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    class CVDetailView(APIView):
        permission_classes = [IsAuthenticated]  


    def get(self, request, pk):
        cv = CV.objects.get(pk=pk, owner=request.user)
        serializer = CVUploadSerializer(cv)
        return Response(serializer.data)