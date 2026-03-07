from django.db import migrations


SITE_NAMES = [
    "Englewood",
    "Hackensack",
    "Mahwah",
    "Ringwood",
    "Saddle Brook",
    "Warehouse (Mahwah)",
    "Warehouse (Saddle Brook)",
]


def sync_sites(apps, schema_editor):
    site_model = apps.get_model("donations", "Site")
    for name in SITE_NAMES:
        site_model.objects.update_or_create(name=name, defaults={"is_active": True})
    site_model.objects.exclude(name__in=SITE_NAMES).update(is_active=False)


class Migration(migrations.Migration):
    dependencies = [
        ("donations", "0003_populate_sites"),
    ]

    operations = [
        migrations.RunPython(sync_sites, migrations.RunPython.noop),
    ]
