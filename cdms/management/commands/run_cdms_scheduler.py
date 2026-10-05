import time

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from cdms.scheduled_sync import ScheduledInventorySync


class Command(BaseCommand):
    help = "Query Inventory at a fixed interval and synchronize new Product data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--interval",
            type=int,
            default=settings.CDMS_SCHEDULE_INTERVAL_SECONDS,
            help="Seconds between Inventory queries.",
        )
        parser.add_argument(
            "--once",
            action="store_true",
            help="Run one query only, then exit.",
        )

    def handle(self, *args, **options):
        interval = options["interval"]
        if interval <= 0:
            raise CommandError("--interval must be greater than zero.")

        sync = ScheduledInventorySync()
        while True:
            try:
                result = sync.run_once()
                self.stdout.write(self.style.SUCCESS(f"CDMS sync: {result}"))
            except Exception as error:
                self.stderr.write(self.style.ERROR(f"CDMS sync failed: {error}"))

            if options["once"]:
                return

            time.sleep(interval)
