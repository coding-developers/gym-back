from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("financial", "0002_producttransaction_delete_subscription_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="payment",
            old_name="company_id",
            new_name="gym_id",
        ),
        migrations.RenameField(
            model_name="producttransaction",
            old_name="company_id",
            new_name="gym_id",
        ),
    ]
