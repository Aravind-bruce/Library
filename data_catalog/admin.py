from django.contrib import admin
from django.http import HttpResponse
from openpyxl import Workbook
from .models import LoginRecord


# -------------------------
#  EXCEL EXPORT FUNCTION
# -------------------------
def export_to_excel(modeladmin, request, queryset):
    wb = Workbook()
    ws = wb.active
    ws.title = "Login Records"

    # Extract model fields dynamically
    columns = [field.name for field in queryset.model._meta.fields]

    # Header row
    ws.append(columns)

    # Data rows
    for obj in queryset:
        row = [getattr(obj, field) for field in columns]
        ws.append(row)

    # Prepare response
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        'attachment; filename="LoginRecord.xlsx"'
    )

    wb.save(response)
    return response


export_to_excel.short_description = "Download selected as Excel (.xlsx)"


# -------------------------
#  LOGIN RECORD ADMIN
# -------------------------
@admin.register(LoginRecord)
class LoginRecordAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'login_date', 'login_time')
    search_fields = ('username', 'email', 'role')
    list_filter = ('role', 'login_date')
    ordering = ('-id',)
    actions = [export_to_excel]   # <-- Excel download option added
