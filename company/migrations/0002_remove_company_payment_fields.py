from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("company", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="company",
            name="day_of_payment",
        ),
        migrations.RemoveField(
            model_name="company",
            name="next_date_payment",
        ),
        migrations.RemoveField(
            model_name="company",
            name="last_date_payment",
        ),
        migrations.RemoveField(
            model_name="company",
            name="status_payment",
        ),
        migrations.RemoveField(
            model_name="company",
            name="type_document",
        ),
        migrations.AlterField(
            model_name="company",
            name="foundation_date",
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name="company",
            name="logo",
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name="company",
            name="avatar_url",
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
    ]
