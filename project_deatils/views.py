from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q, Count
from .models import project_upload
import os
from accounts.decorators import session_login_required


ALLOWED_EXT = ('.pdf',)
@session_login_required
def upload_project(request):
    if request.method == "POST":

        last = project_upload.objects.order_by("-accession_number").first()
        next_acc = 650 if last is None else last.accession_number + 1

        raw_keywords = request.POST.get("keywords", "")
        keyword_list = [k.strip() for k in raw_keywords.split(",") if k.strip()]
        keywords_clean = " - ".join(keyword_list)

        file_obj = request.FILES.get("pdf_file")
        if not file_obj:
            messages.error(request, "Please upload a PDF file.")
            return render(request, "upload_project.html")

        _, ext = os.path.splitext(file_obj.name.lower())
        if ext not in ALLOWED_EXT:
            messages.error(request, "Only PDF files are allowed.")
            return render(request, "upload_project.html")

        proj = project_upload(
            accession_number=next_acc,
            project_type=request.POST.get("project_type"),
            title=request.POST.get("title"),
            keywords=keywords_clean,
            department=request.POST.get("department"),
            submission_date=request.POST.get("submission_date"),
            academic_year=request.POST.get("academic_year"),
            abstract=request.POST.get("abstract"),

            team_leader=request.POST.get("team_leader"),
            team_leader_reg=request.POST.get("team_leader_reg"),

            member1=request.POST.get("member1"),
            member1_reg=request.POST.get("member1_reg"),

            member2=request.POST.get("member2"),
            member2_reg=request.POST.get("member2_reg"),

            member3=request.POST.get("member3"),
            member3_reg=request.POST.get("member3_reg"),

            member4=request.POST.get("member4"),
            member4_reg=request.POST.get("member4_reg"),

            member5=request.POST.get("member5"),
            member5_reg=request.POST.get("member5_reg"),

            member6=request.POST.get("member6"),
            member6_reg=request.POST.get("member6_reg"),
        )

        file_obj.name = f"{next_acc}.pdf"
        proj.pdf_file = file_obj

        proj.save()

        messages.success(request, f"Project Uploaded Successfully! Accession No: {next_acc}")
        return redirect("view_projects")

    return render(request, "upload_project.html")



# =======================================================================
#                        VIEW PROJECTS  ✔ FIXED
# =======================================================================

from django.shortcuts import render
from django.db.models import Q, Count, Case, When, Value, CharField
from .models import project_upload


from django.shortcuts import render
from django.db.models import Q, Count, Case, When, Value, CharField, Avg
from .models import project_upload, ProjectRating

@session_login_required
def view_projects(request):
    dept_map = {
        "Artificial Intelligence and Data Science": "AI&DS",
        "Artificial Intelligence and Machine Learning": "AI&ML",
        "Computer Science Engineering": "CSE",
        "Civil Engineering": "CE",
        "Electronics and Communication Engineering": "ECE",
        "Electrical and Electronics Engineering": "EEE",
        "Information Technology": "IT",
        "Cyber Security": "CY",
        "Mechanical Engineering": "ME",
        "VLSI Design": "VLSI",
        "Mechatronics Engineering": "MT",
    }

    # ✅ Projects with dept_short and ratings
    projects = project_upload.objects.all().order_by("-id").annotate(
        dept_short=Case(
            *(When(department=dept, then=Value(short)) for dept, short in dept_map.items()),
            default=Value(""),
            output_field=CharField()
        ),
        avg_rating=Avg('ratings__rating'),
        total_ratings=Count('ratings')
    )

    # 🔍 FILTERS
    department = request.GET.get("department", "")
    keyword_search = request.GET.get("keyword_search", "")
    academic_year = request.GET.get("academic_year", "")
    common_search = request.GET.get("common_search", "")

    if department:
        projects = projects.filter(dept_short=department)

    if keyword_search:
        projects = projects.filter(keywords__icontains=keyword_search)

    if academic_year:
        projects = projects.filter(academic_year=academic_year)

    if common_search:
        projects = projects.filter(
            Q(title__icontains=common_search) |
            Q(department__icontains=common_search) |
            Q(project_type__icontains=common_search) |
            Q(team_leader__icontains=common_search) |
            Q(keywords__icontains=common_search) |
            Q(accession_number__icontains=common_search)
        )

    academic_years = ["2023-2024", "2024-2025", "2025-2026", "2026-2027", "2027-2028"]

    # 📊 Analytics Data
    minor_dept_stats = list(
        project_upload.objects.filter(project_type="Minor Project")
        .values("department")
        .annotate(count=Count("department"))
    )

    major_dept_stats = list(
        project_upload.objects.filter(project_type="Major Project")
        .values("department")
        .annotate(count=Count("department"))
    )

    total_minor = project_upload.objects.filter(project_type="Minor Project").count()
    total_major = project_upload.objects.filter(project_type="Major Project").count()

    return render(request, "view_projects.html", {
        "projects": projects,
        "academic_years": academic_years,
        "selected_year": academic_year,
        "minor_dept_stats": minor_dept_stats,
        "major_dept_stats": major_dept_stats,
        "total_minor": total_minor,
        "total_major": total_major,
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import project_upload, DownloadRecord
import os
from django.http import FileResponse


@session_login_required
def delete_project(request, pk):
    project = get_object_or_404(project_upload, id=pk)

    # Delete PDF file from MEDIA folder
    if project.pdf_file and os.path.isfile(project.pdf_file.path):
        os.remove(project.pdf_file.path)

    project.delete()
    messages.success(request, "Project deleted successfully!")
    return redirect("view_projects")

from django.http import FileResponse, Http404
from .models import project_upload, DownloadRecord
from accounts.models import Student, Staff, Admin

from django.http import FileResponse, Http404
from .models import project_upload, DownloadRecord
from accounts.models import Student, Staff, Admin
@session_login_required
def download_project(request, project_id):

    # Get project safely
    try:
        project = project_upload.objects.get(id=project_id)
    except project_upload.DoesNotExist:
        raise Http404("Project not found")

    # Get session data
    username = request.session.get("username", "Guest")
    role = request.session.get("role", "Guest")

    # Try to fetch correct user object
    user_obj = None

    try:
        if role == "student":
            user_obj = Student.objects.get(username=username)
        elif role == "staff":
            user_obj = Staff.objects.get(username=username)
        elif role == "admin":
            user_obj = Admin.objects.get(username=username)
    except:
        user_obj = None  # If user not found, stay Guest

    # Save download record
    DownloadRecord.objects.create(
        project=project,
        user=username if user_obj else "Guest",
        role=role if user_obj else "Guest",
        accession_number=project.accession_number,
        project_title=project.title,
        department=project.department,
        project_type=project.project_type,
    )

    # Increase download counter
    project.download_count += 1
    project.save()

    # Return file safely
    return FileResponse(open(project.pdf_file.path, "rb"), as_attachment=True)


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import ProjectRating, project_upload
@session_login_required
def submit_project_rating(request):
    if request.method == "POST":
        project_id = request.POST.get("project_id")
        rating_value = request.POST.get("rating")

        if not project_id or not rating_value:
            return JsonResponse({"status": "error", "message": "Missing rating or project id"})

        project = get_object_or_404(project_upload, id=project_id)

        username = request.session.get("username", "Guest")
        role = request.session.get("role", "Guest")

        ProjectRating.objects.update_or_create(
            project=project,
            user=username,
            defaults={
                "rating": int(rating_value),
                "role": role
            }
        )
        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "invalid request"})

