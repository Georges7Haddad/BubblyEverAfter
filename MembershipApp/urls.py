from django.urls import path

from . import views

app_name = "MembershipApp"

urlpatterns = [
    path("member/login/", views.login_request),
    path("member/logout/", views.logout_request),
    path("member/profile/", views.member_profile),
    path("member/register/", views.register),
    path("leader/dashboard/", views.leader_dashboard),
    path("leader/tickets/", views.leader_tickets),
    path("leader/accommodations/", views.leader_accommodations),
    path("leader/vehicles/", views.leader_vehicles),
    path("leader/<username>/details/", views.leader_search_member),
    path("leader/burns/", views.leader_burns),
    path("leader/membersaccommodations/", views.leader_member_accommodations),
    path("leader/burnsaccommodations/", views.leader_burns_accommodations),
]
