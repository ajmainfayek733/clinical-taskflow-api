from django.core.management.base import BaseCommand

from accounts.models import User
from tasks.models import Tag


class Command(BaseCommand):
    help = "Create or update demo user and baseline tags"

    def handle(self, *args, **options):
        email = "demo.doctor@taskflow.local"
        password = "DoctorDemo123!"

        user, created = User.objects.get_or_create(email=email, defaults={"is_active": True})
        user.set_password(password)
        user.is_active = True
        user.save()

        tags = [
            ("Urgent", "#DC2626"),
            ("Follow-up", "#2563EB"),
            ("Lab", "#7C3AED"),
            ("Documentation", "#0F766E"),
        ]
        for name, color in tags:
            Tag.objects.get_or_create(name=name, defaults={"color": color})

        status = "created" if created else "updated"
        self.stdout.write(self.style.SUCCESS(f"Demo user {status}: {email}"))
        self.stdout.write(self.style.SUCCESS("Password: DoctorDemo123!"))
