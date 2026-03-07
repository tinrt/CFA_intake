from django.db import models


DEFAULT_SITE_NAMES = (
	"Englewood",
	"Hackensack",
	"Mahwah",
	"Ringwood",
	"Saddle Brook",
	"Warehouse (Mahwah)",
	"Warehouse (Saddle Brook)",
)


class Site(models.Model):
	name = models.CharField(max_length=120, unique=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		ordering = ["name"]

	def __str__(self) -> str:
		return self.name

	@classmethod
	def ensure_default_sites(cls) -> None:
		for name in DEFAULT_SITE_NAMES:
			cls.objects.update_or_create(name=name, defaults={"is_active": True})
		cls.objects.exclude(name__in=DEFAULT_SITE_NAMES).update(is_active=False)


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
