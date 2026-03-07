from django import forms

from .models import Donation


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = [
            "site_name",
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
        for name, field in self.fields.items():
            field.widget.attrs.setdefault("class", "form-control")
            field.widget.attrs.setdefault("autocomplete", "off")

        self.fields["notes"].required = True
        self.fields["donor_name"].widget.attrs["list"] = "donor-name-suggestions"
        self.fields["email"].widget.attrs["list"] = "donor-email-suggestions"
