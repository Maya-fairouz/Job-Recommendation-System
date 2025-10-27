from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Roles: seeker, recruiter, admin
    ROLE_CHOICES = (
    ("seeker", "Seeker"),
    ("recruiter", "Recruiter"),
    ("admin", "Admin"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="seeker")


    def is_seeker(self):
        return self.role == "seeker"


    def is_recruiter(self):
        return self.role == "recruiter"