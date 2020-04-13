import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .forms import BubblyMemberForm, MemberSearchForm
from .models import (
    Ticket,
    Accommodation,
    VehiclePass,
    BubblyMember,
    Burn,
    UserAccommodationRelation,
    BurnAccommodationRelation,
)

logger = logging.getLogger(__name__)


def leadership_required(function=None, login_url=None):
    actual_decorator = user_passes_test(lambda u: u.is_authenticated and u.is_leadership, login_url=login_url)
    if function:
        return actual_decorator(function)
    return actual_decorator


def table_view(model):
    objects = model.objects.all()
    secured_tickets = model.objects.filter(secured=True)
    secured_percentage = 100 * secured_tickets.count() / objects.count()
    secured_number = f"{secured_tickets.count()}/{objects.count()}"
    attributes_to_remove = ["burn", "id"]
    fields = [field.name for field in model._meta.get_fields(include_hidden=False, include_parents=True)]
    for attr in attributes_to_remove:
        if attr in fields:
            fields.remove(attr)
    return objects, secured_percentage, secured_number, fields


def login_request(request):
    if not request.user.is_active:
        if request.method == "POST":
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                credentials = form.cleaned_data
                username = credentials["username"]
                password = credentials["password"]
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    member = request.user
                    if member.is_leadership:
                        return redirect("/leader/dashboard/")
                    else:
                        return redirect("/member/profile/")
                else:
                    logger.warning("Invalid Username or Password")
                    messages.warning(request, "Invalid Username or Password")
            else:
                logger.warning("Invalid Username or Password")
                messages.warning(request, "Invalid Username or Password")
        form = AuthenticationForm()
        return render(request=request, template_name="MembershipApp/members_login.html", context={"form": form})
    else:
        return redirect("/member/profile/")


def logout_request(request):
    logout(request)
    return redirect("/member/login/")


def register(request):
    if request.method == "POST":
        bubbly_form = BubblyMemberForm(request.POST)
        if bubbly_form.is_valid():
            bubbly_form.save()
            return redirect("/member/profile/")
        else:
            for msg in bubbly_form.error_messages:
                logger.warning(bubbly_form.error_messages[msg])
                messages.warning(request, bubbly_form.error_messages[msg])
                return render(
                    request=request,
                    template_name="MembershipApp/member_register.html",
                    context={"bubbly_form": bubbly_form},
                )

    bubbly_form = BubblyMemberForm()
    return render(request, "MembershipApp/member_register.html", context={"bubbly_form": bubbly_form})


@login_required(login_url="/member/login/")
def member_profile(request):
    return render(request, "MembershipApp/member_profile.html")


@leadership_required(login_url="/member/login/")
def leader_dashboard(request):
    if request.method == "POST":
        member_search_form = MemberSearchForm(request.POST)
        username = member_search_form.data["username"]
        return redirect(f"/leader/{username}/details")
    member_search_form = MemberSearchForm()
    return render(
        request=request,
        template_name="MembershipApp/leader/leader_dashboard.html",
        context={"member_search_form": member_search_form},
    )


@leadership_required(login_url="/member/profile/")
def leader_search_member(request, username):
    member = BubblyMember.objects.get(username=username)
    return render(request, "MembershipApp/member_profile.html", {"member": member})


@leadership_required(login_url="/member/profile/")
def leader_tickets(request):
    tickets, secured_percentage, secured_number, fields = table_view(Ticket)
    i = 0
    return render(
        request,
        "MembershipApp/leader/leader_tickets.html",
        {
            "tickets": tickets,
            "fields": fields,
            "secured_percentage": secured_percentage,
            "secured_number": secured_number,
            "i": i,
        },
    )


@leadership_required(login_url="/member/profile/")
def leader_vehicles(request):
    vehicles, secured_percentage, secured_number, fields = table_view(VehiclePass)
    return render(
        request,
        "MembershipApp/leader/leader_vehicles.html",
        {
            "vehicles": vehicles,
            "fields": fields,
            "secured_percentage": secured_percentage,
            "secured_number": secured_number,
        },
    )


@leadership_required(login_url="/member/profile/")
def leader_accommodations(request):
    accommodations = Accommodation.objects.all()
    attributes_to_remove = ["burn", "id", "useraccommodationrelation", "members", "burnaccommodationrelation"]
    fields = [field.name for field in Accommodation._meta.get_fields(include_hidden=False, include_parents=True)]
    for attr in attributes_to_remove:
        if attr in fields:
            fields.remove(attr)
    return render(
        request, "MembershipApp/leader/leader_accommodations.html", {"accommodations": accommodations, "fields": fields}
    )


@leadership_required(login_url="/member/profile/")
def leader_burns(request):
    burns = Burn.objects.all()
    attributes_to_remove = ["accommodations", "burnaccommodationrelation"]
    fields = [field.name for field in Burn._meta.get_fields(include_hidden=False, include_parents=True)]
    for attr in attributes_to_remove:
        if attr in fields:
            fields.remove(attr)
    return render(request, "MembershipApp/leader/leader_burns.html", {"burns": burns, "fields": fields})


@leadership_required(login_url="/member/profile/")
def leader_burns_accommodations(request):
    burns = BurnAccommodationRelation.objects.all()
    fields = ["burn", "accommodation"]
    return render(request, "MembershipApp/leader/leader_burns_accommodations.html", {"burns": burns, "fields": fields})


@leadership_required(login_url="/member/profile/")
def leader_member_accommodations(request):
    accommodations = UserAccommodationRelation.objects.all()
    fields = ["member", "accommodation"]
    return render(
        request,
        "MembershipApp/leader/leader_members_accommodations.html",
        {"accommodations": accommodations, "fields": fields},
    )
