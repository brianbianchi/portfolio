from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from ...models import League


class Command(BaseCommand):
    help = "Initializes data"

    def handle(self, *args, **kwargs):
        user = User.objects.filter(is_superuser=True).first()
        League.objects.create(
            name="General",
            description="Site-wide league",
            start_value=100000,
            author=user,
            is_default=True,
        )
