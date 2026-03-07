from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .forms import DonationForm
from .models import Donation


def home(request):
	if not request.user.is_authenticated:
		return redirect("login")
	return redirect("donation-create")


@login_required
def donation_create(request):
	if request.method == "POST":
		form = DonationForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect("donation-log")
	else:
		form = DonationForm(initial={"donation_date": date.today()})

	return render(request, "donations/donation_form.html", {"form": form})


@login_required
def donation_log(request):
	query = request.GET.get("q", "").strip()
	site = request.GET.get("site", "").strip()

	donations = Donation.objects.all()
	if query:
		donations = donations.filter(
			Q(donor_name__icontains=query)
			| Q(email__icontains=query)
			| Q(phone_number__icontains=query)
			| Q(notes__icontains=query)
			| Q(site_name__icontains=query)
		)
	if site:
		donations = donations.filter(site_name__iexact=site)

	site_totals = (
		Donation.objects.values("site_name")
		.annotate(total=Count("id"))
		.order_by("site_name")
	)
	recent_cutoff = date.today() - timedelta(days=30)
	last_30_days_total = Donation.objects.filter(donation_date__gte=recent_cutoff).count()

	context = {
		"donations": donations,
		"query": query,
		"site": site,
		"total_count": donations.count(),
		"all_time_count": Donation.objects.count(),
		"last_30_days_total": last_30_days_total,
		"site_totals": site_totals,
	}
	return render(request, "donations/donation_log.html", context)


@login_required
def donor_suggestions(request):
	term = request.GET.get("q", "").strip()
	if len(term) < 1:
		return JsonResponse({"results": []})

	donors = (
		Donation.objects.filter(Q(donor_name__icontains=term) | Q(email__icontains=term))
		.values("donor_name", "email")
		.annotate(total=Count("id"))
		.order_by("-total", "donor_name")[:10]
	)
	return JsonResponse({"results": list(donors)})
