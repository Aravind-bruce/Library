def user_session_data(request):
    return {
        "username": request.session.get("username"),
        "role": request.session.get("role"),
    }
