from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.recommender.service import get_recommender
from apps.jobs.models import Job


class RecommendView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request):
    # expects either cv_id or raw_text
        cv_id = request.data.get('cv_id')
        raw_text = request.data.get('text')
        if cv_id:
            from apps.cvs.models import CV
            cv = CV.objects.get(id=cv_id, owner=request.user)
            text = cv.extracted_text
        elif raw_text:
            text = raw_text
        else:
            return Response({'error': 'provide cv_id or text'}, status=400)


        rec = get_recommender()
        if not rec.is_ready():
            return Response({'error': 'recommender not ready'}, status=503)
        results = rec.recommend(text, top_n=10)
        # fetch job metadata
        job_ids = [r['job_id'] for r in results]
        jobs = Job.objects.filter(id__in=job_ids)
        job_map = {j.id: j for j in jobs}