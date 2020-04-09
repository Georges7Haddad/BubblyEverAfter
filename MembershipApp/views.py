import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from .forms import BubblyMemberForm

logger = logging.getLogger(__name__)


def leadership_required(function=None, login_url=None):
    actual_decorator = user_passes_test(lambda u: u.is_authenticated and u.is_leadership, login_url=login_url)
    if function:
        return actual_decorator(function)
    return actual_decorator


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
                        return redirect("/member/leader/dashboard/")
                    else:
                        return redirect("/member/profile/")
                else:
                    logger.error(request, "Invalid username or password.")
            else:
                logger.error(request, "Invalid username or password.")
        form = AuthenticationForm()
        return render(request=request, template_name="Membership/members_login.html", context={"form": form})
    else:
        return redirect("/member/profile/")


def logout_request(request):
    logout(request)
    return redirect("/member/login/")


@login_required(login_url="/member/login/")
def member_profile(request):
    return render(request, "Membership/member_profile.html")


@leadership_required(login_url="/member/login/")
def leader_dashboard(request):
    return render(request, "Membership/leader_profile.html")


def register(request):
    if request.method == "POST":
        bubbly_form = BubblyMemberForm(request.POST)
        if bubbly_form.is_valid():
            bubbly_form.save()
            return redirect("/member/profile/")
        else:
            for msg in bubbly_form.error_messages:
                logger.error(bubbly_form.error_messages[msg])
                return render(
                    request=request,
                    template_name="Membership/member_register.html",
                    context={"bubbly_form": bubbly_form},
                )

    bubbly_form = BubblyMemberForm()
    return render(request, "Membership/member_register.html", context={"bubbly_form": bubbly_form})
