from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("modalities", "0002_modality_price"),
    ]

    operations = [
        migrations.RenameField(
            model_name="modality",
            old_name="company_id",
            new_name="gym_id",
        ),
    ]
