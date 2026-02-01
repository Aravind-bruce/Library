from django.shortcuts import render
from .models import LoginRecord
from accounts.decorators import session_login_required

@session_login_required
def view_logins(request):
    records = LoginRecord.objects.all().order_by('-id')
    return render(request, 'view_logins.html', {'records': records})
