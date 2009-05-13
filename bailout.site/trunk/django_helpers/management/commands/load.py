from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = """Similar to loaddata but calls save() explicitly for each record.
    
    This means that custom save logic will run."""
    
    def handle_noargs(self, **options):
        # TODO
        pass
