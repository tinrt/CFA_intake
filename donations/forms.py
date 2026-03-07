from django import forms
from django.db.utils import OperationalError, ProgrammingError

from .models import Donation, Site


class DonationForm(forms.ModelForm):
    site = forms.ModelChoiceField(
        queryset=Site.objects.none(),
        empty_label="Select site",
    )

    class Meta:
        model = Donation
        fields = [
            "site",
            "donation_date",
            "donor_name",
            "email",
            "phone_number",
            "notes",
        ]
        widgets = {
            "donation_date": forms.DateInput(attrs={"type": "date"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            site_queryset = Site.objects.filter(is_active=True).order_by("name")
            # Force a cheap query now so missing table errors are caught here, not in template rendering.
            site_queryset.exists()
            self.fields["site"].queryset = site_queryset
        except (OperationalError, ProgrammingError):
            self.fields["site"].queryset = Site.objects.none()
            self.fields["site"].help_text = "Site table not ready. Run migrations."

        for name, field in self.fields.items():
            field.widget.attrs.setdefault("class", "form-control")
            field.widget.attrs.setdefault("autocomplete", "off")

        self.fields["notes"].required = True
        self.fields["donor_name"].widget.attrs["list"] = "donor-name-suggestions"
        self.fields["email"].widget.attrs["list"] = "donor-email-suggestions"

