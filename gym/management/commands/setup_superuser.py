from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

USERNAME = "admin"
EMAIL = "admin@example.com"
PASSWORD = "Conta123!"


class Command(BaseCommand):
    help = "Creates or updates the superuser with a fixed password for deployment"

    def handle(self, *args, **kwargs):
        User = get_user_model()

        try:
            user, created = User.objects.get_or_create(
                username=USERNAME,
                defaults={"email": EMAIL, "is_staff": True, "is_superuser": True},
            )

            user.set_password(PASSWORD)
            user.is_staff = True
            user.is_superuser = True
            user.save()

            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Superuser '{USERNAME}' created successfully."
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Superuser '{USERNAME}' password updated successfully."
                    )
                )
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Failed to set up superuser '{USERNAME}': {e}")
            )
