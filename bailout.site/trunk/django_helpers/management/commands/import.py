from django.core.management.base import BaseCommand
from optparse import make_option
import os

# Similar to loaddata but calls save() explicitly for each record.
# This means that custom save logic will run.
# Currently, only YAML is supported.
class Command(BaseCommand):

    import_subdir = "import"
    format = "yaml"

    option_list = BaseCommand.option_list + (
        make_option('--verbosity', action='store', dest='verbosity', default='1',
            type='choice', choices=['0', '1', '2'],
            help='Verbosity level; 0=minimal output, 1=normal output, 2=all output'),
    )
    help = 'Import data from <app>/%s/*.%s' % (import_subdir, format)
    args = "app [app ...]"
    
    def handle(self, *app_names, **options):
        from django.db.models import get_models
        from utils.exit_if import exit_if
        from utils.load_yaml_file import load_yaml_file
        from utils.logger import Logger
        from utils.import_model_records import import_model_records

        exit_if(len(app_names) == 0, "Please specify one or more app names.")

        log = Logger(int(options.get('verbosity', 1)))
        log.info("Attempting to import data for these apps: %s" % ", ".join(app_names), 1)
        apps_with_import_dirs = self.get_import_dirs_for_app_names(app_names, log)
        files_found = 0

        for app in apps_with_import_dirs:
            import_dir = apps_with_import_dirs[app]
            log.info("Checking %s for data" % import_dir, 2)
            for model in get_models(app):
                filename = self.convert_model_to_filename(model)
                pathname = os.path.join(import_dir, filename)
                if os.path.exists(pathname):
                    files_found += 1
                    data = load_yaml_file(pathname, log)
                    import_model_records(model, data)

        if files_found == 0:
            log.notice("No files were imported", 0)

    def convert_model_to_filename(self, model):
        """
        Converts a model object to a filename.
        """
        return "%s.%s" % (model.__name__.lower(), self.format)

    def get_import_dirs_for_app_names(self, app_names, log):
        """
        When given a list of app names, returns a dictionary where keys
        are app objects and values are valid import directories.
        """

        from django.db.models import get_app
        from django.core.exceptions import ImproperlyConfigured
        import sys

        import_dirs = {}
        for app_name in app_names:
            try:
                app = get_app(app_name)
            except ImproperlyConfigured:
                log.error("Cannot find app labeled %s" % app_name)
                sys.exit(1)
            import_dir = self.get_import_dir_for_app(app, log)
            if import_dir:
                import_dirs[app] = import_dir
        return import_dirs
    
    def get_import_dir_for_app(self, app, log):
        """
        Returns the import directory for a given app.
        Returns None if the directory does not exist.
        """
        base = os.path.dirname(app.__file__)
        path = os.path.join(base, self.import_subdir)
        return path if os.path.exists(path) else None
