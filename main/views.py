from django.http.response import StreamingHttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.http import request
from .models import Banbury, Curing, Cutter, Fabric, Winder
import json
import time
import csv
from itertools import chain
# Create your views here.

'''
Global variables
'''
# For traversing through the IDs
dash = 1
ban = 1
fab = 1
bead = 1
tread = 1
cur = 1

# For storing last ten values
banList = []
# Dates for the values
bandateList = []
# For case count
banCount = [0, 0, 0]

beadList = []
beaddateList = []
beadCount = [0, 0, 0]

fabList1 = []
fabdateList = []
fabCount1 = [0, 0, 0]
fabList2 = []
fabdateList = []
fabCount2 = [0, 0, 0]

treadList1 = []
treaddateList = []
treadCount1 = [0, 0, 0]
treadList2 = []
treaddateList = []
treadCount2 = [0, 0, 0]

curList1 = []
curdateList = []
curCount1 = [0, 0, 0]
curList2 = []
curdateList = []
curCount2 = [0, 0, 0]

'''
Functions for APIs and Rendering
'''


def dashboard(request):
    # For page rendering

    return render(request, "main/dashboard.html", context={})


def dashboard_json(request):
    # For API

    global dash

    # Incrementing the ID
    x = dash % 1000
    dash += 1

    # Accesong the objects
    banData = Banbury.objects.get(id=x)
    fabData = Fabric.objects.get(id=x)
    beadData = Winder.objects.get(id=x)
    treadData = Cutter.objects.get(id=x)
    curData = Curing.objects.get(id=x)

    # Data dictionary for API
    data = {"dash_ban_width": banData.sheet_width,
            "dash_ban_date": str(banData.dateinserted), "dash_fab_temp": fabData.temperature, "dash_fab_date": str(fabData.dateinserted), "dash_fab_w": fabData.sheet_width, "dash_bead_temp": beadData.temperature,
            "dash_bead_date": str(beadData.dateinserted), "dash_tread_pos": treadData.position_error, "dash_tread_date": str(treadData.dateinserted), "dash_tread_speed": treadData.speed_error, "dash_cur_time": curData.molding_time_mins, "dash_cur_date": str(curData.dateinserted), "dash_cur_temp": curData.temperature}

    return HttpResponse(json.dumps(data))


def banbury(request):
    return render(request, "main/banbury.html")


def banbury_json(request):

    global ban, banList, bandateList, banCount

    x = ban % 1000
    ban += 1

    banData = Banbury.objects.get(id=x)

    width = banData.sheet_width

    banList.append(width)

    # Popping the first element at every tenth increment
    if len(banList) >= 10:
        while len(banList) > 10:
            bandateList.pop(0)
            banList.pop(0)

    # Storing counts
    if width > 16 and width < 24:
        banCount[0] += 1
    elif width == 16 or width == 24:
        banCount[1] += 1
    else:
        banCount[2] += 1

    # Appending date in string format
    bandateList.append(banData.dateinserted.strftime("%m/%d/%Y, %H:%M:%S"))

    data = {"banList": banList, "bandateList": bandateList,
            "sheet_width": banData.sheet_width, "dateinserted": str(banData.dateinserted), "banCount": banCount}
    return HttpResponse(json.dumps(data))


def fabCalendar(request):
    return render(request, "main/fabCalendar.html")


def fabric_json(request):

    global fab, fabList1, fabList2, fabdateList, fabCount1, fabCount2

    x = fab % 1000
    fab += 1

    fabData = Fabric.objects.get(id=x)

    width = fabData.sheet_width
    temp = fabData.temperature

    fabList1.append(temp)
    fabList2.append(width)

    if len(fabList1) >= 10:
        while len(fabList1) > 10:
            fabdateList.pop(0)
            fabList1.pop(0)
            fabList2.pop(0)

    if temp < 600 and temp > 500:
        fabCount1[0] += 1
    elif temp == 600 or temp == 500:
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


def beadWinder_json(request):

    global bead, beadList, beaddateList, beadCount

    x = bead % 1000
    bead += 1

    beadData = Winder.objects.get(id=x)

    temp = beadData.temperature
    beadList.append(temp)

    if len(beadList) >= 10:
        while len(beadList) > 10:
            beaddateList.pop(0)
            beadList.pop(0)

    if temp < 700 and temp > 600:
        beadCount[0] += 1
    elif temp == 700 or temp == 600:
        beadCount[1] += 1
    else:
        beadCount[2] += 1

    beaddateList.append(beadData.dateinserted.strftime("%m/%d/%Y, %H:%M:%S"))

    data = {"beadList": beadList, "beaddateList": beaddateList,
            "temperature": beadData.temperature, "dateinserted": str(beadData.dateinserted), "beadCount": beadCount}

    return HttpResponse(json.dumps(data))


def treadCutter(request):
    return render(request, "main/tread.html")


def treadCutter_json(request):

    global tread, treadList1, treadList2, treaddateList, treadCount1, treadCount2

    x = tread % 1000
    tread += 1

    treadData = Cutter.objects.get(id=x)

    pos = treadData.position_error
    speed = treadData.speed_error

    treadList1.append(pos)
    treadList2.append(speed)

    if len(treadList1) >= 10:
        while len(treadList1) > 10:
            treaddateList.pop(0)
            treadList1.pop(0)
            treadList2.pop(0)

    if pos > -2 and pos < 2:
        treadCount1[0] += 1
    elif pos == -2 or pos == 2:
        treadCount1[1] += 1
    else:
        treadCount1[2] += 1

    if speed > -3 and speed < 3:
        treadCount2[0] += 1
    elif speed == -3 or speed == 3:
        treadCount2[1] += 1
    else:
        treadCount2[2] += 1

    treaddateList.append(treadData.dateinserted.strftime("%m/%d/%Y, %H:%M:%S"))

    data = {"treadList1": treadList1, "treadList2": treadList2, "treaddateList": treaddateList,
            "tread_pos": pos, "tread_date": str(treadData.dateinserted), "tread_speed": speed, "treadCount1": treadCount1, "treadCount2": treadCount2}

    return HttpResponse(json.dumps(data))


def curing(request):
    return render(request, "main/curing.html")


def Curing_json(request):

    global cur, curList1, curList2, curdateList, curCount1, curCount2

    x = cur % 1000
    cur += 1

    curData = Curing.objects.get(id=x)

    time = curData.molding_time_mins
    temp = curData.temperature

    curList1.append(time)
    curList2.append(temp)

    if len(curList1) >= 10:
        while len(curList2) > 10:
            curdateList.pop(0)
            curList1.pop(0)
            curList2.pop(0)

    if time > 30 and time < 35:
        curCount1[0] += 1
    elif time == 30 or time == 35:
        curCount1[1] += 1
    else:
        curCount1[2] += 1

    if temp > 200 and temp < 250:
        curCount2[0] += 1
    elif temp == 200 or temp == 250:
        curCount2[1] += 1
    else:
        curCount2[2] += 1

    curdateList.append(curData.dateinserted.strftime("%m/%d/%Y, %H:%M:%S"))

    data = {"curList1": curList1, "curList2": curList2, "curdateList": curdateList,
            "cur_time": time, "cur_date": str(curData.dateinserted), "cur_temp": temp, "curCount1": curCount1, "curCount2": curCount2}

    return HttpResponse(json.dumps(data))


class Echo:
    @staticmethod
    def write(value):
        return value


def stats(request):
    global ban, fab, bead, tread, cur

    header = (['Banbury Date&Time', 'Banbury Sheet Width', 'Fabric Calender Date&Time', 'Fabric Temperature', 'Fabric Width', 'Bead Winder Date&Time', 'Bead Temperature',
               'Treading Cutter Date&Time', 'Tread Position Error', 'Tread Speed Error', 'Curing Machine Date&Time', 'Curing Moulding Temperature', 'Curing Moulding Time'],)

    Data_csv = []

    for (a, b, c, d, e) in zip(range(1, ban+1), range(1, fab+1), range(1, bead+1), range(1, tread+1), range(1, cur+1)):

        banData = Banbury.objects.get(id=a)
        fabData = Fabric.objects.get(id=b)
        beadData = Winder.objects.get(id=c)
        treadData = Cutter.objects.get(id=d)
        curData = Curing.objects.get(id=e)

        data = ([str(banData.dateinserted), banData.sheet_width, str(fabData.dateinserted), fabData.temperature, fabData.sheet_width, str(beadData.dateinserted),
                 beadData.temperature, str(treadData.dateinserted), treadData.position_error, treadData.speed_error, str(curData.dateinserted), curData.temperature, curData.molding_time_mins])
        Data_csv.append(data)

    psuedo_buffer = Echo()
    writer = csv.writer(psuedo_buffer)
    response = StreamingHttpResponse(
        (writer.writerow(row) for row in chain(header, Data_csv)), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Current_Report.csv"'
    response['status'] = 200
    return response
