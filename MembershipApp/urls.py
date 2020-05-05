from django.urls import path

from . import views

app_name = "MembershipApp"

urlpatterns = [
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request),
    path("register/", views.register),
    path("member/<username>/", views.member_profile),
    path("member/<username>/tickets/", views.tickets_view),
    path("member/<username>/vehicles/", views.vehicles_view),
    path("member/<username>/accommodations/", views.accommodations_view),
    path("member/<username>/burns/", views.burns_view),
    # path("ticket/<pk>/", views),
    path("ticket/<pk>/edit/", views.edit_ticket),
    # path("ticket/insert/", views.add_ticket),
    # path("vehicle_pass/<pk>/", views),
    path("vehicle_pass/<pk>/edit/", views.edit_vehicle),
    # path("vehicle_pass/insert/", views.add_vehicle),
    # path("accommodation/<pk>/", views),
    path("accommodation/<pk>/edit/", views.edit_accommodation),
    # path("accommodation/insert/", views.add_accommodation),
    # path("burn/<pk>/", views),
    path("burn/<pk>/edit/", views.edit_burn),
    # path("burn/insert/", views.add_burn),
    path("leader/dashboard/", views.leader_dashboard),
    path("leader/tickets/", views.leader_tables),
    path("leader/vehicles/", views.leader_tables),
    path("leader/burns/", views.leader_tables),
    path("leader/burnsaccommodations/", views.leader_burns_accommodations),
]
