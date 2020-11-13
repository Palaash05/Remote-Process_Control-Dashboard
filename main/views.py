from django.shortcuts import render
from django.http import HttpResponse
from django.http import request
from .models import Banbury, Fabric
import json
import time
# Create your views here.


dash = 1
ban = 1
fab = 1
banList = []
bandateList = []
banCount = [0, 0, 0]

fabList1 = []
fabdateList = []
fabCount1 = [0, 0, 0]
fabList2 = []
fabdateList = []
fabCount2 = [0, 0, 0]


def dashboard(request):
    return render(request, "main/dashboard.html", context={})


def dashboard_json(request):
    global dash

    x = dash % 100
    dash += 1
    banData = Banbury.objects.get(id=x)
    fabData = Fabric.objects.get(id=x)

    data = {"ban_width": banData.sheet_width,
            "ban_date": str(banData.dateinserted), "fab_temp": fabData.temperature, "fab_date": str(fabData.dateinserted), "fab_w": fabData.sheet_width}
    return HttpResponse(json.dumps(data))


def banbury(request):
    return render(request, "main/banbury.html")


def banbury_json(request):

    global ban, banList, bandateList, banCount

    if len(banList) >= 10:
        bandateList = bandateList[-11:-1]
        banList = banList[-11:-1]

    x = ban % 100
    ban += 1
    banData = Banbury.objects.get(id=x)
    width = banData.sheet_width
    banList.append(width)

    if width > 18 and width < 22:
        banCount[0] += 1
    elif width == 22 or width == 10:
        banCount[1] += 1
    else:
        banCount[2] += 1
    print(banCount)
    bandateList.append(banData.dateinserted.strftime("%m/%d/%Y, %H:%M:%S"))

    data = {"banList": banList, "bandateList": bandateList,
            "sheet_width": banData.sheet_width, "dateinserted": str(banData.dateinserted), "banCount": banCount}
    return HttpResponse(json.dumps(data))


def fabCalendar(request):
    return render(request, "main/fabCalendar.html")


def fabric_json(request):

    global fab, fabList1, fabList2, fabdateList, fabCount1, fabCount2

    if len(fabList1) >= 10:
        fabdateList = fabdateList[-11:-1]
        fabList1 = fabList1[-11:-1]
        fabList2 = fabList2[-11:-1]

    x = fab % 100
    fab += 1
    fabData = Fabric.objects.get(id=x)
    width = fabData.sheet_width
    temp = fabData.temperature
    fabList1.append(temp)
    fabList2.append(width)

    if temp > 520 and temp < 500:
        fabCount1[0] += 1
    elif temp == 520 or temp == 500:
        fabCount1[1] += 1
    else:
        fabCount1[2] += 1

    if width > 0.5 and width < 1.5:
        fabCount2[0] += 1
    elif width == 0.5 or width == 1.5:
        fabCount2[1] += 1
    else:
        fabCount2[2] += 1

    fabdateList.append(fabData.dateinserted.strftime("%m/%d/%Y, %H:%M:%S"))

    data = {"fabList1": fabList1, "fabList2": fabList2, "fabdateList": fabdateList,
            "fab_temp": temp, "fab_date": str(fabData.dateinserted), "fab_w": width, "fabCount1": fabCount1, "fabCount2": fabCount2}
    return HttpResponse(json.dumps(data))


def beadWinder(request):
    return render(request, "main/beadWinder.html")


def tread(request):
    return render(request, "main/tread.html")


def curing(request):
    return render(request, "main/curing.html")


def stats(request):
    return render(request, "main/stats.html")
