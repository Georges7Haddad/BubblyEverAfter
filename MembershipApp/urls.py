from django.urls import path

from . import views

app_name = "MembershipApp"

urlpatterns = [
    path("", views.members),
]
