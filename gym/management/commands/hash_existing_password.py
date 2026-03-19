from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password, is_password_usable
from gym.models import User


class Command(BaseCommand):
    help = "Aplica hash nas senhas em texto puro existentes no banco"

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        total = 0

        for user in users:
            if not is_password_usable(user.password):  # já tem hash? pula
                user.password = make_password(user.password)
                user.save(update_fields=["password"])
                total += 1
                self.stdout.write(f"  ✔ {user.email}")

        self.stdout.write(self.style.SUCCESS(f"\n{total} senha(s) atualizadas."))
