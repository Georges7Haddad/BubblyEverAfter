from django.urls import path

from . import views

app_name = "MembershipApp"

urlpatterns = [
    path("login/", views.login_request),
    path("profile", views.member_profile),
    path("leader/profile", views.leader_profile),
]