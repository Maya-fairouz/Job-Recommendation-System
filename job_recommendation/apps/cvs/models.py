from django.db import models
from django.conf import settings


class CV(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cvs')
    file = models.FileField(upload_to='cvs/')
    extracted_text = models.TextField(blank=True)
    language = models.CharField(max_length=16, blank=True)
    parsed_skills = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)


    def __str__(self):
        return f"CV {self.id} — {self.owner.username}"


    class Interaction(models.Model):
        # record clicks, saves, applied events for feedback
        cv = models.ForeignKey(CV, on_delete=models.CASCADE, related_name='interactions')
        job_id = models.IntegerField() # denormalized job id
        action = models.CharField(max_length=50) # 'click','save','apply'
        created_at = models.DateTimeField(auto_now_add=True)