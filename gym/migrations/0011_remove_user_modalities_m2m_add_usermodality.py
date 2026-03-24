import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gym", "0010_user_status_payment_user_deleted_at"),
    ]

    operations = [
        # Remove a M2M legada (gym_user_modalities → gym_modalitie)
        migrations.RemoveField(
            model_name="user",
            name="modalities",
        ),
        # Cria tabela de relacionamento com modalities.Modality por ID inteiro
        migrations.CreateModel(
            name="UserModality",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ("modality_id", models.IntegerField(db_index=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="user_modalities",
                        to="gym.user",
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "modality_id")},
            },
        ),
    ]
