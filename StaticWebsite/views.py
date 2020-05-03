from django.contrib import messages
from django.shortcuts import render, redirect

from MembershipApp.forms import ContactForm, CreateEvent
from MembershipApp.models import BubblyEvents
from MembershipApp.views import leadership_required


def index(request):
    return render(request, "MembershipApp/index.html")


def burningman(request):
    return render(request, "MembershipApp/burningman.html")


def legal(request):
    return render(request, "MembershipApp/community_ethos.html")


def about(request):
    return render(request, "MembershipApp/about.html")


def contact(request):
    if request.method == "POST":
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return redirect("/home")
        else:
            return render(
                request=request, template_name="MembershipApp/contact.html", context={"contact_form": contact_form},
            )

    contact_form = ContactForm()
    return render(request, "MembershipApp/contact.html", context={"contact_form": contact_form})


def display_events(request):
    events = BubblyEvents.objects.all()
    context = {"events": events}
    return render(request, "MembershipApp/display_events.html", context)


@leadership_required(login_url="/member/login/")
def leader_dashboard(request):
    return render(request, "MembershipApp/leader_profile.html")


def create_event(request):
    if request.method == "POST":
        event_form = CreateEvent(request.POST)
        if event_form.is_valid():
            event_form.save()
            return redirect("/display_events")
        else:
            messages.warning(request, "Please fill all fields appropriately ")
            return render(
                request=request, template_name="MembershipApp/createvent.html", context={"CreateEvent": CreateEvent},
            )

    event_form = CreateEvent()
    return render(request, "MembershipApp/createvent.html", context={"event_form": event_form})
