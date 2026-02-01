from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout as auth_logout

from .models import Student, Staff, Admin, Approval
from data_catalog.models import LoginRecord
from .decorators import session_login_required


# --------------------------------------------------------
# SIGNUP
# --------------------------------------------------------
def signup_view(request):
    if request.method == "POST":
        role = request.POST["role"]
        username = request.POST["username"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        password = request.POST["password"]

        # STUDENT SIGNUP
        if role == "student":
            department = request.POST["department"]
            year = request.POST["year"]

            Student.objects.create(
                username=username,
                email=email,
                phone=phone,
                password=password,
                department=department,
                year=year,
                role="student",
                is_approved=False
            )

            Approval.objects.create(
                username=username,
                role="student",
                is_approved=False
            )

        # STAFF SIGNUP
        elif role == "staff":
            department = request.POST["department"]

            Staff.objects.create(
                username=username,
                email=email,
                phone=phone,
                password=password,
                department=department,
                role="staff",
                is_approved=False
            )

            Approval.objects.create(
                username=username,
                role="staff",
                is_approved=False
            )

        # ADMIN SIGNUP (NO approval needed)
        else:
            Admin.objects.create(
                username=username,
                email=email,
                phone=phone,
                password=password,
                role="admin"
            )

        messages.success(request, "Signup successful! (Wait for admin approval)")
        return redirect("login")

    return render(request, "signup.html")


# --------------------------------------------------------
# LOGIN
# --------------------------------------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        role = request.POST["role"]

        user = None

        if role == "student":
            user = Student.objects.filter(username=username, password=password).first()
        elif role == "staff":
            user = Staff.objects.filter(username=username, password=password).first()
        else:
            user = Admin.objects.filter(username=username, password=password).first()

        if not user:
            messages.error(request, "Invalid credentials")
            return redirect("login")

        # Approval check
        if role != "admin" and not user.is_approved:
            messages.error(request, "You are not approved yet!")
            return redirect("login")

        # Save session
        request.session["username"] = username
        request.session["role"] = role

        # ⭐ IP ADDRESS
        ip_address = get_client_ip(request)

        # ⭐ SAVE LOGIN RECORD
        from datetime import datetime
        now = datetime.now()

        LoginRecord.objects.create(
            username=username,
            role=role,
            email=user.email,
            ip_address=ip_address,          # ⭐ STORED
            login_date=now.strftime("%d/%m/%Y"),
            login_time=now.strftime("%H:%M:%S"),
        )

        return redirect("home")

    return render(request, "login.html")


# --------------------------------------------------------
# PENDING APPROVAL LIST (Admin Only)
# --------------------------------------------------------
@session_login_required
def pending_approvals(request):
    pending_list = Approval.objects.filter(is_approved=False)
    final_data = []

    for item in pending_list:
        email = "-"
        department = "-"

        if item.role == "student":
            s = Student.objects.filter(username=item.username).first()
            if s:
                email = s.email
                department = s.department

        elif item.role == "staff":
            st = Staff.objects.filter(username=item.username).first()
            if st:
                email = st.email
                department = st.department

        final_data.append({
            "id": item.id,
            "username": item.username,
            "role": item.role,
            "email": email,
            "department": department
        })

    return render(request, "pending_approvals.html", {"pending": final_data})

# --------------------------------------------------------
# APPROVE USERS
# --------------------------------------------------------
@session_login_required
def approve_user(request, approval_id):
    # Only admin can approve
    if request.session.get("role") != "admin":
        messages.error(request, "Access Denied!")
        return redirect("home")

    approval = get_object_or_404(Approval, id=approval_id)

    # Approve in original table
    if approval.role == "student":
        Student.objects.filter(username=approval.username).update(is_approved=True)

    elif approval.role == "staff":
        Staff.objects.filter(username=approval.username).update(is_approved=True)

    # Mark as approved in Approval table
    approval.is_approved = True
    approval.save()

    messages.success(request, f"{approval.username} approved successfully!")
    return redirect("pending_approvals")


# --------------------------------------------------------
# HOME PAGE
# --------------------------------------------------------
@session_login_required
def home(request):
    if "username" not in request.session:
        return redirect("login")

    context = {
        "username": request.session.get("username"),
        "role": request.session.get("role"),
    }

    return render(request, "home.html", context)


# --------------------------------------------------------
# LOGOUT
# --------------------------------------------------------
def logout_view(request):
    request.session.flush()  # Clear custom session
    auth_logout(request)     # Django logout
    return redirect("login")

def delete_user(request, approval_id):
    approval = get_object_or_404(Approval, id=approval_id)

    # Delete from original table
    if approval.role == "student":
        Student.objects.filter(username=approval.username).delete()

    elif approval.role == "staff":
        Staff.objects.filter(username=approval.username).delete()

    # Remove the approval entry
    approval.delete()

    return redirect("pending_approvals")

@session_login_required
def members_list(request):

    # Approved members
    approved_students = Student.objects.filter(is_approved=True).order_by("department")
    approved_staff = Staff.objects.filter(is_approved=True)

    return render(request, "members_list.html", {
        "approved_students": approved_students,
        "approved_staff": approved_staff,
    })

# --------------------------------------------------------
# DELETE STUDENT
# --------------------------------------------------------
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    # Delete from Approval table also
    Approval.objects.filter(username=student.username).delete()

    student.delete()
    messages.success(request, "Student deleted successfully!")
    return redirect("members_list")


# --------------------------------------------------------
# DELETE STAFF
# --------------------------------------------------------
def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff, id=staff_id)

    # Delete from Approval table also
    Approval.objects.filter(username=staff.username).delete()

    staff.delete()
    messages.success(request, "Staff deleted successfully!")
    return redirect("members_list")

def index(request):
    return render(request, "index.html")

from django.core.mail import send_mail
from django.shortcuts import render
from django.http import JsonResponse

from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse

def contact_email(request):
    if request.method == "POST":
        user_name = request.POST.get("name")
        user_email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        final_message = f"""
You received a new message from your website contact form:

Name: {user_name}
Email: {user_email}
Subject: {subject}

Message:
{message}
        """

        send_mail(
            f"New Contact Form Message: {subject}",
            final_message,
            "aravind.bruce.20@gmail.com",  # FROM
            ["aravind.bruce.20@gmail.com"], # TO (your email)
            fail_silently=False,
        )

        return HttpResponse("Message sent successfully!")

    return HttpResponse("Invalid Request", status=400)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
