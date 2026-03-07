from django.db import migrations, models


def migrate_site_name_to_site_fk(apps, schema_editor):
    donation_model = apps.get_model("donations", "Donation")
    site_model = apps.get_model("donations", "Site")

    for donation in donation_model.objects.all().iterator():
        site_name = (donation.site_name or "").strip()
        if site_name:
            site_obj, _ = site_model.objects.get_or_create(
                name=site_name,
                defaults={"is_active": True},
            )
        else:
            site_obj, _ = site_model.objects.get_or_create(
                name="Unassigned",
                defaults={"is_active": False},
            )
        donation.site_id = site_obj.id
        donation.save(update_fields=["site"])


class Migration(migrations.Migration):
    dependencies = [
        ("donations", "0004_sync_site_names"),
    ]

    operations = [
        migrations.AddField(
            model_name="donation",
            name="site",
            field=models.ForeignKey(
                null=True,
                on_delete=models.PROTECT,
                related_name="donations",
                to="donations.site",
            ),
        ),
        migrations.RunPython(migrate_site_name_to_site_fk, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="donation",
            name="site_name",
        ),
        migrations.AlterField(
            model_name="donation",
            name="site",
            field=models.ForeignKey(
                on_delete=models.PROTECT,
                related_name="donations",
                to="donations.site",
            ),
        ),
    ]
