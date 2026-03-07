from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("donations/new/", views.donation_create, name="donation-create"),
    path("donations/log/", views.donation_log, name="donation-log"),
    path("api/donor-suggestions/", views.donor_suggestions, name="donor-suggestions"),
]
