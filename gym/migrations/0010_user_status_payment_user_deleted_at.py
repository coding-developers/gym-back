from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gym", "0009_remove_company_last_date_payment_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="status_payment",
            field=models.CharField(
                choices=[
                    ("active", "Active"),
                    ("inactive", "Inactive"),
                    ("overdue", "Overdue"),
                ],
                max_length=20,
                null=True,
                blank=True,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="deleted_at",
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="date_of_birth",
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="gender",
            field=models.CharField(
                choices=[("male", "Male"), ("female", "Female"), ("other", "Other")],
                max_length=10,
                null=True,
                blank=True,
            ),
        ),
    ]
