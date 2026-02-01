from django.db import models
import os

class project_upload(models.Model):

    PROJECT_TYPES = [
        ("Major Project", "Major Project"),
        ("Minor Project", "Minor Project"),
    ]

    ACADEMIC_YEARS = [
        ("2023-2024", "2023-2024"),
        ("2024-2025", "2024-2025"),
        ("2025-2026", "2025-2026"),
        ("2026-2027", "2026-2027"),
        ("2027-2028", "2027-2028"),
    ]

    accession_number = models.IntegerField(unique=True)

    project_type = models.CharField(max_length=50, choices=PROJECT_TYPES)
    title = models.CharField(max_length=255)
    keywords = models.CharField(max_length=300)
    abstract = models.TextField(blank=True, null=True)
    department = models.CharField(max_length=200)
    submission_date = models.DateField()
    academic_year = models.CharField(max_length=20, choices=ACADEMIC_YEARS)

    # Leader
    team_leader = models.CharField(max_length=100)
    team_leader_reg = models.CharField(max_length=20)

    # Members
    member1 = models.CharField(max_length=100)
    member1_reg = models.CharField(max_length=20)

    member2 = models.CharField(max_length=100)
    member2_reg = models.CharField(max_length=20)

    member3 = models.CharField(max_length=100)
    member3_reg = models.CharField(max_length=20)

    member4 = models.CharField(max_length=100, blank=True, null=True)
    member4_reg = models.CharField(max_length=20, blank=True, null=True)

    member5 = models.CharField(max_length=100, blank=True, null=True)
    member5_reg = models.CharField(max_length=20, blank=True, null=True)

    member6 = models.CharField(max_length=100, blank=True, null=True)
    member6_reg = models.CharField(max_length=20, blank=True, null=True)

    pdf_file = models.FileField(upload_to="projects/")

    download_count = models.IntegerField(default=0)


    def __str__(self):
        return f"{self.accession_number} - {self.title}"

class DownloadRecord(models.Model):
    project = models.ForeignKey(project_upload, on_delete=models.CASCADE)
    user = models.CharField(max_length=200)   # username or Guest
    role = models.CharField(max_length=100, blank=True, null=True)  # STUDENT / FACULTY / ADMIN
    downloaded_at = models.DateTimeField(auto_now_add=True)

    accession_number = models.IntegerField()
    project_title = models.CharField(max_length=255)
    department = models.CharField(max_length=200)
    project_type = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.project_title} downloaded by {self.user} ({self.role})"
    
class ProjectRating(models.Model):
    project = models.ForeignKey(
        project_upload,
        on_delete=models.CASCADE,
        related_name="ratings"
    )

    user = models.CharField(max_length=200)   # username or Guest
    role = models.CharField(max_length=100, blank=True, null=True)

    rating = models.IntegerField()  # 1 to 5 stars

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("project", "user")  # ⭐ one rating per user per project

    def __str__(self):
        return f"{self.project.title} - {self.rating}⭐ by {self.user}"
