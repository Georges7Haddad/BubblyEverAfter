from django.urls import path

from . import views

app_name = "MembershipApp"

urlpatterns = [
    path("login/", views.login_request),
    path("logout/", views.logout_request),
    path("profile/", views.member_profile),
    path("leader/dashboard/", views.leader_dashboard),
    path("register/", views.register),
    path("leader/tickets/", views.leader_tickets),
    path("leader/accommodations/", views.leader_accommodations),
    path("leader/vehicles/", views.leader_vehicles),
    path("leader/<username>/details/", views.leader_member_details),
]
