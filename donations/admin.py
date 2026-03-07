from django.contrib import admin

from .models import Donation


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
	list_display = ("site_name", "donation_date", "donor_name", "email", "phone_number")
	search_fields = ("site_name", "donor_name", "email", "phone_number", "notes")
	list_filter = ("site_name", "donation_date")
