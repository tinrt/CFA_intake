from django import forms
from .models import Site

class SiteSelectForm(forms.Form):
    site = forms.ModelChoiceField(
        queryset=Site.objects.filter(is_active=True).order_by("name"),
        empty_label="Select site",
        required=True,
        widget=forms.Select(attrs={"class": "form-control"})
    )
