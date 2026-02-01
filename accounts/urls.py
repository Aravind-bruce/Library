from django.urls import path
from .views import index, contact_email, signup_view, login_view, home, pending_approvals, approve_user, logout_view, delete_user, members_list, delete_student, delete_staff

urlpatterns = [
    path('', index, name='index'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home, name='home'),

    # Pending Approval List
    path('pending-approvals/', pending_approvals, name='pending_approvals'),

    # Approve a user
    path('approve/<int:approval_id>/', approve_user, name='approve_user'),

    path('delete/<int:approval_id>/', delete_user, name='delete_user'),

    path('members-list/', members_list, name='members_list'),

    path('delete-student/<int:student_id>/', delete_student, name='delete_student'),
    path('delete-staff/<int:staff_id>/', delete_staff, name='delete_staff'),
    path('contact_email/', contact_email, name='contact_email'),
]
