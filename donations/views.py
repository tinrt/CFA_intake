

import csv
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

@login_required
def donation_export_csv(request):
    # Use same filters as donation_log
    query = request.GET.get("q", "").strip()
    site = request.GET.get("site", "").strip()
    donor_type = request.GET.get("donor_type", "").strip()
    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()

    donations = Donation.objects.select_related("site").all()
    if query:
        donations = donations.filter(
            Q(donor_name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone_number__icontains=query)
            | Q(notes__icontains=query)
            | Q(site__name__icontains=query)
        )
    if site:
        donations = donations.filter(site__name__iexact=site)
    if donor_type:
        donations = donations.filter(donor_type=donor_type)
    if date_from:
        donations = donations.filter(donation_date__gte=date_from)
    if date_to:
        donations = donations.filter(donation_date__lte=date_to)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="donations.csv"'
    writer = csv.writer(response)
    writer.writerow(["Date", "Site", "Donor", "Type", "Email", "Phone", "Notes"])
    for d in donations:
        writer.writerow([
            d.donation_date,
            d.site.name,
            d.donor_name,
            d.donor_type,
            d.email,
            d.phone_number,
            d.notes,
        ])
    return response



@login_required
def donation_export_pdf(request):
    # Use same filters as donation_log
    query = request.GET.get("q", "").strip()
    site = request.GET.get("site", "").strip()
    donor_type = request.GET.get("donor_type", "").strip()
    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()

    donations = Donation.objects.select_related("site").all()
    if query:
        donations = donations.filter(
            Q(donor_name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone_number__icontains=query)
            | Q(notes__icontains=query)
            | Q(site__name__icontains=query)
        )
    if site:
        donations = donations.filter(site__name__iexact=site)
    if donor_type:
        donations = donations.filter(donor_type=donor_type)
    if date_from:
        donations = donations.filter(donation_date__gte=date_from)
    if date_to:
        donations = donations.filter(donation_date__lte=date_to)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="donations.pdf"'

    buffer = []
    c = canvas.Canvas(response, pagesize=landscape(letter))
    width, height = landscape(letter)

    # Table header
    columns = ["Date", "Site", "Donor", "Type", "Email", "Phone", "Notes"]
    col_widths = [1*inch, 1.5*inch, 1.5*inch, 1*inch, 2*inch, 1.2*inch, 3*inch]
    x = 0.5 * inch
    y = height - 0.75 * inch
    for i, col in enumerate(columns):
        c.setFont("Helvetica-Bold", 11)
        c.drawString(x, y, col)
        x += col_widths[i]

    # Table rows
    y -= 0.3 * inch
    c.setFont("Helvetica", 10)
    for d in donations:
        x = 0.5 * inch
        row = [
            str(d.donation_date),
            d.site.name,
            d.donor_name,
            d.donor_type,
            d.email,
            d.phone_number,
            (d.notes[:60] + ("..." if len(d.notes) > 60 else "")),
        ]
        for i, value in enumerate(row):
            c.drawString(x, y, value if value else "-")
            x += col_widths[i]
        y -= 0.25 * inch
        if y < 0.75 * inch:
            c.showPage()
            y = height - 0.75 * inch
            c.setFont("Helvetica-Bold", 11)
            x = 0.5 * inch
            for i, col in enumerate(columns):
                c.drawString(x, y, col)
                x += col_widths[i]
            y -= 0.3 * inch
            c.setFont("Helvetica", 10)

    c.save()
    return response
from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Count, F, Q
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .forms import DonationForm
from .models import Donation, Site


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return redirect("donation-create")


@login_required
def donation_create(request):
    if request.method == "POST":
        form = DonationForm(request.POST)
        if form.is_valid():
            donation = form.save()
            if donation.email:
                send_mail(
                    subject="Donation Verification",
                    message=(
                        "Thank you for your donation to Center for Food Action.\n\n"
                        f"Donor: {donation.donor_name}\n"
                        f"Site: {donation.site.name}\n"
                        f"Date: {donation.donation_date}\n"
                        f"Phone: {donation.phone_number or '-'}\n"
                        f"Notes: {donation.notes}\n"
                    ),
                    from_email=None,
                    recipient_list=[donation.email],
                    fail_silently=True,
                )
            return redirect("donation-log")
    else:
        form = DonationForm(initial={"donation_date": date.today()})

    return render(request, "donations/donation_form.html", {"form": form})


@login_required
def donation_log(request):
    query = request.GET.get("q", "").strip()
    site = request.GET.get("site", "").strip()
    donor_type = request.GET.get("donor_type", "").strip()
    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()

    donations = Donation.objects.select_related("site").all()
    if query:
        donations = donations.filter(
            Q(donor_name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone_number__icontains=query)
            | Q(notes__icontains=query)
            | Q(site__name__icontains=query)
        )
    if site:
        donations = donations.filter(site__name__iexact=site)
    if donor_type:
        donations = donations.filter(donor_type=donor_type)
    if date_from:
        donations = donations.filter(donation_date__gte=date_from)
    if date_to:
        donations = donations.filter(donation_date__lte=date_to)

    site_totals = (
        Donation.objects.values(site_name=F("site__name"))
        .annotate(total=Count("id"))
        .order_by("site_name")
    )
    recent_cutoff = date.today() - timedelta(days=30)
    last_30_days_total = Donation.objects.filter(donation_date__gte=recent_cutoff).count()

    donor_type_choices = [
        ("", "All Categories"),
        ("Civic", "Civic"),
        ("Religious", "Religious"),
        ("Corporate", "Corporate"),
        ("Individual", "Individual"),
    ]

    context = {
        "donations": donations,
        "query": query,
        "site": site,
        "donor_type": donor_type,
        "date_from": date_from,
        "date_to": date_to,
        "donor_type_choices": donor_type_choices,
        "active_sites": Site.objects.filter(is_active=True).order_by("name"),
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
