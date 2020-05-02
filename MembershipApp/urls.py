from django.conf.urls import url
from django.urls import path, include

from . import views


app_name = "MembershipApp"

urlpatterns = [
    path("login/", views.login_request),
    path("logout/", views.logout_request),
    path("profile/", views.member_profile),
    path("leader/dashboard/", views.leader_dashboard),
    path("register/", views.register),

]

