from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook

from .models import Student, Staff, Admin as AdminUser


# -------------------------
#  EXCEL EXPORT FUNCTION
# -------------------------
def export_to_excel(modeladmin, request, queryset):
    wb = Workbook()
    ws = wb.active
    ws.title = "Data Export"

    # Get column names dynamically
    columns = [field.name for field in queryset.model._meta.fields]

    # Write header
    ws.append(columns)

    # Write row data
    for obj in queryset:
        row = [getattr(obj, field) for field in columns]
        ws.append(row)

    # Prepare HttpResponse
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename="{queryset.model.__name__}.xlsx"'
    wb.save(response)
    return response


export_to_excel.short_description = "Download selected as Excel (.xlsx)"


# -------------------------
#  STUDENT ADMIN
# -------------------------
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'role', 'department', 'year')
    search_fields = ('username', 'email', 'department', 'year')
    list_filter = ('role', 'department', 'year')
    actions = [export_to_excel]   # <-- Excel download button


# -------------------------
#  STAFF ADMIN
# -------------------------
@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'role', 'department')
    search_fields = ('username', 'email', 'department')
    list_filter = ('role', 'department')
    actions = [export_to_excel]   # <-- Excel download button


# -------------------------
#  ADMIN USER ADMIN
# -------------------------
@admin.register(AdminUser)
class AdminUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone', 'role')
    search_fields = ('username', 'email')
    list_filter = ('role',)
    actions = [export_to_excel]   # <-- Excel download button
