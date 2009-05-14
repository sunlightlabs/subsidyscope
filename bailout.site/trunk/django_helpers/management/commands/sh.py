from django.core.management.base import NoArgsCommand
from django.core.management import call_command
import os.path

# This custom command works for the built-in python shell,
# but it does work out of the box for iPython.
#
# The default python shell will load a script designated by
# PYTHONSTARTUP but ipython does not (by default).
#
# To make this custom command work with iPython, add the
# following to .ipython/ipy_user_conf.py:
#
# ==========
# 
# def main():
#     # ...
#     # ...
#     run_pythonstartup_script()
#
# # Running this method will make us (more) compatible with the default
# # python shell.  It executes the file designed by PYTHONSTARTUP.
# def run_pythonstartup_script():
#     import os
#     script = os.environ.get('PYTHONSTARTUP')
#     if script:
#         print "Running PYTHONSTARTUP script..."
#         ip.ex('execfile("%s")' % script)
#
# ==========
#
class Command(NoArgsCommand):
    help = "Runs shell with all app models imported"
    
    def handle_noargs(self, **options):
        our_path = os.path.abspath(os.path.dirname(__file__))
        os.environ["PYTHONSTARTUP"] = os.path.abspath(
            os.path.join(our_path, '..', 'extras', 'startup.py'))

        verbosity = int(options.get('verbosity', 1))
        call_command('shell', verbosity=verbosity)
