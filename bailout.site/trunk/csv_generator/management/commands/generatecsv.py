from django.core.management.base import NoArgsCommand
from csv_generator import manager

class Command(NoArgsCommand):
    help = "Can be run as a cronjob or directly to generate new CSV data files."

    def handle_noargs(self, **options):
        manager.generate_data()