from django.db import models


class Donation(models.Model):
	site_name = models.CharField(max_length=120)
	donation_date = models.DateField()
	donor_name = models.CharField(max_length=120)
	email = models.EmailField(blank=True)
	phone_number = models.CharField(max_length=30, blank=True)
	notes = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-donation_date", "-created_at"]

	def __str__(self) -> str:
		return f"{self.donor_name} ({self.donation_date})"
