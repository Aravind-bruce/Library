from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook
from .models import project_upload, DownloadRecord, ProjectRating


# --------------------------------------------------
#  EXCEL EXPORT FUNCTION (Reusable for any model)
# --------------------------------------------------
def export_to_excel(modeladmin, request, queryset):
    wb = Workbook()
    ws = wb.active
    ws.title = modeladmin.model.__name__

    # Get field names
    fields = [field.name for field in queryset.model._meta.fields]

    ws.append(fields)  # Header row

    for obj in queryset:
        row = []
        for field in fields:
            value = getattr(obj, field)

            # Convert FileField/ImageField into a readable string
            if hasattr(value, "url"):  # FileField or ImageField
                value = value.url  # or str(value) if you want path

            # Convert non-primitive types to string
            elif not isinstance(value, (int, float, str, bool)):
                value = str(value)

            row.append(value)

        ws.append(row)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        f'attachment; filename="{modeladmin.model.__name__}.xlsx"'
    )

    wb.save(response)
    return response


# --------------------------------------------------
#  PROJECT UPLOAD ADMIN
# --------------------------------------------------
@admin.register(project_upload)
class ProjectUploadAdmin(admin.ModelAdmin):
    list_display = (
        "accession_number",
        "title",
        "project_type",
        "academic_year",
        "department",
        "team_leader",
        "team_leader_reg",
        "keywords",
    )
    
    list_filter = (
        "project_type",
        "academic_year",
        "department",
    )
    
    search_fields = (
        "accession_number",
        "title",
        "keywords",
        "team_leader",
        "team_leader_reg",
        "member1",
        "member2",
        "member3",
        "member4",
        "member5",
        "member6",
        "member1_reg",
        "member2_reg",
        "member3_reg",
        "member4_reg",
        "member5_reg",
        "member6_reg",
    )

    ordering = ("-accession_number",)
    actions = [export_to_excel]   # <-- Excel Export Added


# --------------------------------------------------
#  DOWNLOAD RECORD ADMIN
# --------------------------------------------------
@admin.register(DownloadRecord)
class DownloadRecordAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "user",
        "role",
        "downloaded_at",
        "accession_number",
        "project_title",
        "department",
        "project_type",
    )
    
    search_fields = ("user", "project_title", "department", "project_type", "role")
    list_filter = ("role", "department", "project_type", "downloaded_at")
    ordering = ("-downloaded_at",)
    actions = [export_to_excel]   # <-- Excel Export Added


# --------------------------------------------------
#  PROJECT RATING ADMIN
# --------------------------------------------------
@admin.register(ProjectRating)
class ProjectRatingAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "user",
        "role",
        "rating",
        "created_at",
    )

    search_fields = ("user", "project__title", "role")
    list_filter = ("role", "rating", "created_at")
    ordering = ("-created_at",)
    actions = [export_to_excel]   # <-- Excel Export Added
