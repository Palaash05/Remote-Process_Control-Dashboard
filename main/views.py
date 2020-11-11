from django.shortcuts import render
from django.http import HttpResponse
from django.http import request
# Create your views here.


def dashboard(request):
    # return HttpResponse("Something")
    return render(request, "main/dashboard.html", context={})


def banbury(request):
    return render(request, "main/banbury.html")


def fabCalendar(request):
    return render(request, "main/fabCalendar.html")


def beadWinder(request):
    return render(request, "main/beadWinder.html")


def tread(request):
    return render(request, "main/tread.html")


def curing(request):
    return render(request, "main/curing.html")


def stats(request):
    return render(request, "main/stats.html")
