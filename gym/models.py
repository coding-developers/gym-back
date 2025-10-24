from django.db import models
from django.utils import timezone
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta


class Company(models.Model):
    name = models.CharField(max_length=255)
    day_of_payment = models.IntegerField()
    next_date_payment = models.DateTimeField(null=True, blank=True)
    last_date_payment = models.DateTimeField(null=True, blank=True)
    type_document = models.CharField(max_length=255, null=True)
    document = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=255, null=True)
    email = models.CharField(max_length=255)
    foundation_date = models.DateTimeField(null=True)
    logo = models.CharField(max_length=255, null=True)
    founder = models.ForeignKey(
        "User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="founded_companies",
    )
    phone_number = models.CharField(max_length=255, null=True)
    avatar_url = models.CharField(max_length=255, null=True)
    day_of_payment = models.IntegerField()
    status_payment = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Se day_of_payment estiver definido, calcular next_date_payment
        if self.day_of_payment:
            today = timezone.now().date()

            # Se já houver next_date_payment, usar como referência
            if not self.next_date_payment:
                # calcula o próximo dia de pagamento a partir de hoje
                year = today.year
                month = today.month
                # se o dia já passou esse mês, vai para o próximo mês
                if today.day > self.day_of_payment:
                    month += 1
                    if month > 12:
                        month = 1
                        year += 1
                self.next_date_payment = datetime(year, month, self.day_of_payment)

            self.last_date_payment = self.next_date_payment - relativedelta(months=1)

        super().save(*args, **kwargs)


class Modalitie(models.Model):
    gym = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="modalities",
    )
    status = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class User(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]
    LEVEL_CHOICES = [
        ("client", "Client"),
        ("admin", "Admin"),
        ("personal", "Personal"),
    ]

    gym = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="users",
    )
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, null=True)
    full_name = models.CharField(max_length=255)
    level = models.CharField(max_length=255, choices=LEVEL_CHOICES, null=True)
    document = models.CharField(max_length=255, null=True)
    date_of_birth = models.DateTimeField(null=True)
    modalities = models.ManyToManyField(Modalitie, blank=True, related_name="users")
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=255, null=True)
    avatar_url = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name
