"""scout URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from main import views

app_name = "main"

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('banbury', views.banbury, name="banbury"),
    path('fabCalendar', views.fabCalendar, name="fabCalendar"),
    path('beadWinder', views.beadWinder, name="beadWinder"),
    path('tread', views.treadCutter, name="tread"),
    path('curing', views.curing, name="curing"),
    path('stats', views.stats, name="stats"),
    path('dash_json', views.dashboard_json, name="dash_json"),
    path('ban_json', views.banbury_json, name="ban_json"),
    path('fab_json', views.fabric_json, name="fab_json"),
    path('bead_json', views.beadWinder_json, name="bead_json"),
    path('tread_json', views.treadCutter_json, name="tread_json"),
    path('cur_json', views.Curing_json, name="cur_json"),

]
