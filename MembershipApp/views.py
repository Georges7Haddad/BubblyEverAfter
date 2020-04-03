from django.shortcuts import render


def members(request):
    return render(request, "Membership/members.html")
