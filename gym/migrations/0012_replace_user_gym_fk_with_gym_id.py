import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gym", "0011_remove_user_modalities_m2m_add_usermodality"),
    ]

    operations = [
        # Remove FK gym → gym_company e adiciona gym_id como IntegerField
        migrations.RemoveField(
            model_name="user",
            name="gym",
        ),
        migrations.AddField(
            model_name="user",
            name="gym_id",
            field=models.IntegerField(db_index=True, default=0),
            preserve_default=False,
        ),
        # Remove tabelas legadas que não são mais usadas
        migrations.DeleteModel(
            name="Modalitie",
        ),
        migrations.DeleteModel(
            name="Company",
        ),
    ]
