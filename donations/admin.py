from django.contrib import admin

from .models import Donation, Site


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("site", "donation_date", "donor_name", "email", "phone_number")
    search_fields = ("site__name", "donor_name", "email", "phone_number", "notes")
    list_filter = ("site", "donation_date")
