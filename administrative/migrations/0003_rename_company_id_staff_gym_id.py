from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("administrative", "0002_rename_student_id_staff_user_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="staff",
            old_name="company_id",
            new_name="gym_id",
        ),
    ]
