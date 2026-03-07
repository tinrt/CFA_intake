from django.db import migrations


SITE_NAMES = [
    "Englewood",
    "Hackensack",
    "Mahwah",
    "Paterson - Catholic Charities",
    "Pop-up Distribution",
    "Ringwood",
    "Saddle Brook",
    "Warehouse (Mahwah)",
    "Warehouse (Saddle Brook)",
]


def populate_sites(apps, schema_editor):
    site_model = apps.get_model("donations", "Site")
    for name in SITE_NAMES:
        site_model.objects.get_or_create(name=name, defaults={"is_active": True})


class Migration(migrations.Migration):
    dependencies = [
        ("donations", "0002_site"),
    ]

    operations = [
        migrations.RunPython(populate_sites, migrations.RunPython.noop),
    ]
