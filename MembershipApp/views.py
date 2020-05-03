import datetime
import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404

from .forms import (
    BubblyMemberForm,
    MemberSearchForm,
    YearFilterForm,
    YearGroupForm,
    BurnForm,
    TicketForm,
    VehiclePassForm,
    AccommodationForm,
)
from .models import Ticket, VehiclePass, BubblyMember, Burn, BurnAccommodationRelation, Accommodation, \
    UserAccommodationRelation

logger = logging.getLogger(__name__)


def leadership_required(function=None, login_url=None):
    actual_decorator = user_passes_test(lambda u: u.is_authenticated and u.is_leadership, login_url=login_url)
    if function:
        return actual_decorator(function)
    return actual_decorator


def progress_bar(model):
    burns = Burn.objects.filter(year=int(datetime.datetime.now().year))
    objects = []
    secured_object = 0
    if model == Ticket:
        for burn in burns:
            objects.append(burn.ticket)
            if burn.ticket.secured:
                secured_object += 1
        total = len(objects)
    elif model == VehiclePass:
        for burn in burns:
            try:
                objects.append(burn.vehicle_pass)
                if burn.vehicle_pass.secured:
                    secured_object += 1
            except:
                secured_object = secured_object
        total = len(objects)
    else:
        secured_object = burns.count()
        total = model.objects.all().count()

    secured_percentage = 100 * secured_object / total
    secured_number = f"{secured_object}/{total}"
    return secured_percentage, secured_number


def table_view(model, year, attributes_to_remove_param):
    objects = []
    secured_object = 0
    if year is None:
        burns = Burn.objects.all()
    else:
        burns = get_list_or_404(Burn, year=year)

    if model == Ticket:
        for burn in burns:
            objects.append(burn.ticket)
            if burn.ticket.secured:
                secured_object += 1
    elif model == VehiclePass:
        for burn in burns:
            objects.append(burn.vehicle_pass)
            if burn.vehicle_pass.secured:
                secured_object += 1
    else:
        objects = burns
    secured_percentage = 100 * secured_object / len(objects)
    secured_number = f"{secured_object}/{len(objects)}"
    attributes_to_remove = attributes_to_remove_param
    fields = [field.name for field in model._meta.get_fields(include_hidden=False, include_parents=True)]
    for attr in attributes_to_remove:
        if attr in fields:
            fields.remove(attr)
    return burns, objects, fields, secured_percentage, secured_number


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
                        return redirect(f"/member/{username}")
                else:
                    logger.warning("Invalid Username or Password")
                    messages.warning(request, "Invalid Username or Password")
            else:
                logger.warning("Invalid Username or Password")
                messages.warning(request, "Invalid Username or Password")
        form = AuthenticationForm()
        return render(request=request, template_name="MembershipApp/members_login.html", context={"form": form})
    else:
        return redirect(f"/member/{request.user.username}/")


def logout_request(request):
    logout(request)
    return redirect("/login/")


def register(request):
    if request.method == "POST":
        bubbly_form = BubblyMemberForm(request.POST)
        if bubbly_form.is_valid():
            bubbly_form.save()
            return redirect("/login/")
        else:
            for msg in bubbly_form.error_messages:
                logger.warning(bubbly_form.error_messages[msg])
                messages.warning(request, bubbly_form.error_messages[msg])
            return render(
                request=request,
                template_name="MembershipApp/member_register.html",
                context={"bubbly_form": bubbly_form},
            )
    else:
        bubbly_form = BubblyMemberForm()
        return render(request, "MembershipApp/member_register.html", context={"bubbly_form": bubbly_form})


@login_required(login_url="/login/")
def member_profile(request, username):
    try:
        member = get_object_or_404(BubblyMember, username=username)
        if request.method == "POST":
            bubbly_form = BubblyMemberForm(data=request.POST, instance=member)
            if bubbly_form.is_valid():
                bubbly_form.save(commit=False)
                member.save()
                return redirect(f"/member/{username}/")
            else:
                for msg in bubbly_form.error_messages:
                    logger.warning(bubbly_form.error_messages[msg])
                    messages.warning(request, bubbly_form.error_messages[msg])
                return render(
                    request=request,
                    template_name="MembershipApp/member/member_profile.html",
                    context={"bubbly_form": bubbly_form},
                )
        else:
            bubbly_form = BubblyMemberForm(
                initial={
                    "username": member.username,
                    "birthday": member.birthday,
                    "gender_identity": member.gender_identity,
                    "ethnic_identity": member.ethnic_identity,
                    "country": member.country,
                    "city": member.city,
                    "phone_number": member.phone_number,
                    "facebook": member.facebook,
                    "paypal_email": member.paypal_email,
                    "playa_name": member.playa_name,
                    "burning_man_profile_email": member.burning_man_profile_email,
                    "is_virgin_burner": member.is_virgin_burner,
                    "years_attending_burning_man": member.years_attending_burning_man,
                    "referring_member": member.referring_member,
                    "allergies": member.allergies,
                    "medical_issues": member.medical_issues,
                    "first_name": member.first_name,
                    "last_name": member.last_name,
                }
            )
            return render(
                request, "MembershipApp/member/member_profile.html", {"member": member, "bubbly_form": bubbly_form}
            )
    except ObjectDoesNotExist as err:
        logger.warning(f"Did not find user {username}")
        return HttpResponseNotFound(f"Did not find user {username}")


@leadership_required(login_url="/login/")
def leader_dashboard(request):
    tickets_percentage, tickets_number = progress_bar(Ticket)
    vehicles_percentage, vehicles_number = progress_bar(VehiclePass)
    burn_percentage, burn_number = progress_bar(BubblyMember)

    burns = Burn.objects.filter(year=datetime.datetime.now().year)
    members = [str(i).replace("'s Burn", "") for i in burns]

    strike_deposit = list(burns.values_list("strike_deposit", flat=True))
    strike_deposit_paid = list(burns.values_list("strike_deposit_paid", flat=True))
    strike_deposit_paid = [-i for i in strike_deposit_paid]

    camp_dues = list(burns.values_list("camp_dues", flat=True))
    camp_dues_paid = list(burns.values_list("camp_dues_paid", flat=True))
    camp_dues_paid = [-i for i in camp_dues_paid]

    total_camp_dues = burns.aggregate(Sum("camp_dues"))["camp_dues__sum"]
    total_camp_dues_paid = burns.aggregate(Sum("camp_dues_paid"))["camp_dues_paid__sum"]

    if request.method == "POST":
        member_search_form = MemberSearchForm(request.POST)
        username = member_search_form.data["username"]
        return redirect(f"/member/{username}/")
    member_search_form = MemberSearchForm()
    return render(
        request=request,
        template_name="MembershipApp/leader/leader_dashboard.html",
        context={
            "member_search_form": member_search_form,
            "tickets_percentage": tickets_percentage,
            "tickets_number": tickets_number,
            "vehicles_percentage": vehicles_percentage,
            "vehicles_number": vehicles_number,
            "burn_percentage": burn_percentage,
            "burn_number": burn_number,
            "members": members,
            "camp_dues": camp_dues,
            "camp_dues_paid": camp_dues_paid,
            "strike_deposit": strike_deposit,
            "strike_deposit_paid": strike_deposit_paid,
            "total_camp_dues": total_camp_dues,
            "total_camp_dues_paid": total_camp_dues_paid,
        },
    )


@leadership_required(login_url="/login/")
def leader_tables(request):
    if request.method == "POST":
        year_form = YearFilterForm(request.POST)
        if year_form.is_valid():
            year = year_form.cleaned_data["year"]
        else:
            year = datetime.datetime.now().year
    else:
        year = datetime.datetime.now().year

    if request.path == "/leader/tickets/":
        burns, tickets, fields, secured_percentage, secured_number = table_view(Ticket, year, ["burn", "id"])

        paginator = Paginator(burns, 2)
        page = request.GET.get("page")
        try:
            burns = paginator.page(page)
        except PageNotAnInteger:
            burns = paginator.page(1)
        except EmptyPage:
            burns = paginator.page(paginator.num_pages)
        year_form = YearFilterForm()
        return render(
            request,
            "MembershipApp/leader/leader_tickets.html",
            {
                "tickets": tickets,
                "fields": fields,
                "burns": burns,
                "secured_percentage": secured_percentage,
                "secured_number": secured_number,
                "year_form": year_form,
                "year": year,
            },
        )
    elif request.path == "/leader/vehicles/":
        burns, vehicles, fields, secured_percentage, secured_number = table_view(VehiclePass, year, ["burn", "id"])

        paginator = Paginator(burns, 10)
        page = request.GET.get("page")
        try:
            burns = paginator.page(page)
        except PageNotAnInteger:
            burns = paginator.page(1)
        except EmptyPage:
            burns = paginator.page(paginator.num_pages)

        year_form = YearFilterForm()
        return render(
            request,
            "MembershipApp/leader/leader_vehicles.html",
            {
                "vehicles": vehicles,
                "fields": fields,
                "burns": burns,
                "secured_percentage": secured_percentage,
                "secured_number": secured_number,
                "year_form": year_form,
                "year": year,
            },
        )
    elif request.path == "/leader/burns/":
        attributes_to_remove = [
            "id",
            "accommodations",
            "burnaccommodationrelation",
            "camp_dues",
            "camp_dues_paid",
            "strike_deposit",
            "strike_deposit_paid",
            "meal_plan_paid",
            "year",
            "notes",
        ]
        burns, burn, fields, secured_percentage, secured_number = table_view(Burn, year, attributes_to_remove)

        paginator = Paginator(burns, 10)
        page = request.GET.get("page")
        try:
            burns = paginator.page(page)
        except PageNotAnInteger:
            burns = paginator.page(1)
        except EmptyPage:
            burns = paginator.page(paginator.num_pages)

        year_form = YearFilterForm()
        return render(
            request,
            "MembershipApp/leader/leader_burns.html",
            {"burns": burns, "fields": fields, "year_form": year_form, "year": year},
        )


@leadership_required(login_url="/login/")
def leader_burns_accommodations(request):
    if request.method == "POST":
        year_group_form = YearGroupForm(request.POST)
        if year_group_form.is_valid():
            year = year_group_form.cleaned_data["year"]
            group = year_group_form.cleaned_data["group"]
        else:
            year = datetime.datetime.now().year
            group = "Burn"
    else:
        year = datetime.datetime.now().year
        group = "Burn"

    try:
        burns = Burn.objects.filter(year=year)
    except:
        return HttpResponseBadRequest("Please go back and correct the year entered")

    accomm = []
    for burn in burns:
        accomm.append(BurnAccommodationRelation.objects.filter(burn=burn))
    year_group_form = YearGroupForm()
    return render(
        request,
        "MembershipApp/leader/leader_burns_accommodations.html",
        {"burns": burns, "accomm": accomm, "year_group_form": year_group_form, "year": year, "group": group},
    )


@login_required(login_url="/login/")
def tickets_view(request, username):
    try:
        member = BubblyMember.objects.get(username=username)
        tickets = Ticket.objects.filter(member=member)
        if request.method == "POST":
            ticket_form = TicketForm(request.POST)
            if ticket_form.is_valid():
                ticket_form.save()
                return redirect(f"/member/{request.user}/tickets")
            else:
                logger.warning("Invalid Form")
                messages.warning(request, "Invalid Form")
        else:
            ticket_form = TicketForm()
            return render(request, "MembershipApp/member/member_tickets.html",
                          {"ticket_form": ticket_form, "tickets": tickets, "username": username})
    except ObjectDoesNotExist as err:
        logger.warning(f"Did not find user {username}")
        return HttpResponseNotFound(f"Did not find user {username}")


@login_required(login_url="/login/")
def vehicles_view(request, username):
    try:
        member = BubblyMember.objects.get(username=username)
        vehicles = VehiclePass.objects.filter(member=member)
        if request.method == "POST":
            vehicle_form = VehiclePassForm(request.POST)
            if vehicle_form.is_valid():
                vehicle_form.save()
                return redirect(f"/member/{request.user}/vehicles")
            else:
                logger.warning("Invalid Form")
                messages.warning(request, "Invalid Form")
        else:
            vehicle_form = VehiclePassForm()
            return render(request, "MembershipApp/member/member_vehicles.html",
                          {"vehicle_form": vehicle_form, "vehicles": vehicles, "username": username})
    except ObjectDoesNotExist as err:
        logger.warning(f"Did not find user {username}")
        return HttpResponseNotFound(f"Did not find user {username}")


@login_required(login_url="/login/")
def accommodations_view(request, username):
    try:
        member = BubblyMember.objects.get(username=username)
        accommodations = Accommodation.objects.filter(members=member)
        if request.method == "POST":
            accommodation_form = AccommodationForm(request.POST)
            if accommodation_form.is_valid():
                accommodation_form.save()
                accom = Accommodation.objects.get(name=accommodation_form.cleaned_data["name"])
                UserAccommodationRelation.objects.create(accommodation=accom, member=member)
                return redirect(f"/member/{request.user}/accommodations")
            else:
                logger.warning("Invalid Form")
                messages.warning(request, "Invalid Form")
        else:
            accommodation_form = AccommodationForm()
            return render(
                request, "MembershipApp/member/member_accommodations.html",
                {"accommodation_form": accommodation_form, "accommodations": accommodations, "username": username}
            )
    except ObjectDoesNotExist as err:
        logger.warning(f"Did not find user {username}")
        return HttpResponseNotFound(f"Did not find user {username}")


@login_required(login_url="/login/")
def burns_view(request, username):
    try:
        member = BubblyMember.objects.get(username=username)
        burns = Burn.objects.filter(member=member)
        if request.method == "POST":
            burn_form = BurnForm(request.POST)
            if burn_form.is_valid():
                burn_form.save()
                return redirect(f"/member/{request.user}/burns")
            else:
                logger.warning("Invalid Form")
                messages.warning(request, "Invalid Form")
        else:
            burn_form = BurnForm()
            return render(request, "MembershipApp/member/member_burns.html",
                          {"burn_form": burn_form, "burns": burns, "username": username})
    except ObjectDoesNotExist as err:
        logger.warning(f"Did not find user {username}")
        return HttpResponseNotFound(f"Did not find user {username}")


@login_required(login_url="/login/")
def edit_ticket(request, pk):
    if request.method == "POST":
        ticket = get_object_or_404(Ticket, id=pk)
        ticket_form = TicketForm(request.POST, instance=ticket)
        if ticket_form.is_valid():
            ticket_form.save(commit=False)
            ticket.save()
            return redirect(f"/member/{request.user}/tickets")
        else:
            logger.warning("Invalid Form")
            messages.warning(request, "Invalid Form")
    else:
        ticket_form = TicketForm()
        return render(request, "MembershipApp/member/edit_ticket.html", {"ticket_form": ticket_form})


@login_required(login_url="/login/")
def edit_vehicle(request, pk):
    if request.method == "POST":
        vehicle = get_object_or_404(VehiclePass, id=pk)
        vehicle_form = VehiclePassForm(request.POST, instance=vehicle)
        if vehicle_form.is_valid():
            vehicle_form.save(commit=False)
            vehicle.save()
            return redirect(f"/member/{request.user}/vehicles")
        else:
            logger.warning("Invalid Form")
            messages.warning(request, "Invalid Form")
    else:
        vehicle_form = VehiclePassForm()
        return render(request, "MembershipApp/member/edit_vehicle.html", {"vehicle_form": vehicle_form})


@login_required(login_url="/login/")
def edit_accommodation(request, pk):
    if request.method == "POST":
        accommodation = get_object_or_404(Accommodation, id=pk)
        accommodation_form = AccommodationForm(request.POST, instance=accommodation)
        if accommodation_form.is_valid():
            accommodation_form.save(commit=False)
            accommodation.save()
            return redirect(f"/member/{request.user}/accommodations")
        else:
            logger.warning("Invalid Form")
            messages.warning(request, "Invalid Form")
    else:
        accommodation_form = AccommodationForm()
        return render(
            request, "MembershipApp/member/edit_accommodation.html", {"accommodation_form": accommodation_form}
        )


@login_required(login_url="/login/")
def edit_burn(request, pk):
    if request.method == "POST":
        burn = get_object_or_404(Burn, id=pk)
        burn_form = BurnForm(request.POST, instance=burn)
        if burn_form.is_valid():
            burn_form.save(commit=False)
            burn.save()
            return redirect(f"/member/{request.user}/burns")
        else:
            logger.warning("Invalid Form")
            messages.warning(request, "Invalid Form")
    else:
        burn_form = BurnForm()
        return render(request, "MembershipApp/member/edit_burn.html", {"burn_form": burn_form})
