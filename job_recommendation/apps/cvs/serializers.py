# serializers.py
from rest_framework import serializers
from .models import CV


class CVUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CV
        fields = ['id','file','processed','extracted_text','parsed_skills']
        read_only_fields = ['processed','extracted_text','parsed_skills']

