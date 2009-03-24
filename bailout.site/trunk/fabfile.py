# Subsidyscope fabfile

# TODO: add private decorator once fabric adds support for it
def subsidyscope_setup():
    "Sets up initial environment variables"

    # === NOTE: 'pull' methods assume a ~/.fabric file that looks like the following ===
    # subsidyscope_local_project_root = /Users/thomaslee/Projects/subsidyscope/bailout.site/trunk
    # subsidyscope_local_ssh_keyfile_for_staging = /Users/username/.ssh/id_dsa
    # subsidyscope_local_login_for_staging = subsidyscope@monkey.sunlightlabs.com

    # fabric connection variables
    set( fab_hosts = ['subsidyscope.com'], fab_user='subsidyscope' )

    # environment variables. prefix is what machine they are used on -- sorry if it's confusing
    set( staging_project_root='/home/subsidyscope/lib/python/subsidyscope', staging_python_root='/home/subsidyscope/lib/python')
    set( live_project_root='/home/subsidyscope/lib/python/subsidyscope', live_python_root='/home/subsidyscope/lib/python', live_ssh_keyfile_for_staging='/home/subsidyscope/.ssh/monkey_id_dsa', live_login_for_staging='subsidyscope@monkey.sunlightlabs.com')
    set( local_project_root=get('subsidyscope_local_project_root'), local_ssh_keyfile_for_staging=get('subsidyscope_local_ssh_keyfile_for_staging'), local_login_for_staging=get('subsidyscope_local_login_for_staging') ) 


# TODO: add private decorator once fabric adds support for it
def push_fixture(fixture_name=None, restart_server=False):
    subsidyscope_setup()
    
    "Moves the specified fixture from staging to production"
    if fixture_name is None:
        prompt('app_name', 'What application fixture would you like to push from staging to the live server?')
        fixture_name = ENV['app_name']
    
    # generate, transfer and sync fixture
    set(fixture=fixture_name)
    run('ssh -i $(live_ssh_keyfile_for_staging) $(live_login_for_staging) "export PYTHONPATH=$(staging_python_root):$PYTHONPATH && python $(staging_project_root)/manage.py dumpdata $(fixture) > $(staging_project_root)/data/$(fixture).json"')
    run('scp -C -i $(live_ssh_keyfile_for_staging) $(live_login_for_staging):$(staging_project_root)/data/$(fixture).json $(live_project_root)/data/$(fixture).json')
    run('export PYTHONPATH=$(live_python_root):$PYTHONPATH && python $(live_project_root)/manage.py loaddata $(live_project_root)/data/$(fixture).json')
    
    if restart_server is True:
        run('/home/subsidyscope/run-this.sh')


# TODO: add private decorator once fabric adds support for it
def pull_fixture(fixture_name=None):
    if fixture_name is None:
        prompt('app_name', 'What application fixture would you like to retrieve and install locally?')
        fixture_name = ENV['app_name']

    subsidyscope_setup()
      
    q = get('local_project_root',None)
    if q is None:
        local('echo Local configuration settings not detected. Have you set up ~/.fabric ?')
        return
    
    # generate, transfer and sync fixture
    set(fixture=fixture_name)
    local('ssh -i $(local_ssh_keyfile_for_staging) $(local_login_for_staging) "export PYTHONPATH=$(staging_python_root):$PYTHONPATH && python $(staging_project_root)/manage.py dumpdata $(fixture) > $(staging_project_root)/data/$(fixture).json"')
    local('scp -C -i $(local_ssh_keyfile_for_staging) $(local_login_for_staging):$(staging_project_root)/data/$(fixture).json $(local_project_root)/data/$(fixture).json')
    local('python $(local_project_root)/manage.py loaddata $(local_project_root)/data/$(fixture).json')
    
    
def pull_tarp(): 
    "Downloads and installs data supporting the TARP database."
    subsidyscope_setup()
    pull_fixture('etl')
    pull_fixture('bailout')


def pull_documents(): 
    "Downloads and installs data supporting the document repository. Does not transfer PDFs."
    subsidyscope_setup()
    pull_fixture('bailout_pdfs')

def pull_email_list_to_local():
    "Pulls the list of subscribers from the staging server to the local box"
    subsidyscope_setup()
    pull_fixture('spammer')
    
def pull_email_list_to_staging():
    "Pulls the list of subscribers from the production server to the staging server"
    # NOTE: this is the ONLY fab task that should pull data from the live server to staging
    #       (hence the lack of a more generalized solution)
    subsidyscope_setup()
    set(fixture='spammer')
    run('export PYTHONPATH=$(live_python_root):$PYTHONPATH && python $(live_project_root)/manage.py dumpdata $(fixture) > $(live_project_root)/data/$(fixture).json')
    run('scp -C -i $(live_ssh_keyfile_for_staging) $(live_project_root)/data/$(fixture).json $(live_login_for_staging):$(staging_project_root)/data/$(fixture).json')
    run('ssh -i $(live_ssh_keyfile_for_staging) $(live_login_for_staging) "export PYTHONPATH=$(staging_python_root):$PYTHONPATH && python $(staging_project_root)/manage.py loaddata $(staging_project_root)/data/$(fixture).json"')


def push_documents():
    "Pushes files and fixtures supporting the bailout_pdfs application from staging to production."
    # setup -- all commands go through a shell connection to the live site
    subsidyscope_setup()
    
    # sync PDF files
    run('rsync -r -v -z --exclude=".*" -e "ssh -i $(live_ssh_keyfile_for_staging)" $(live_login_for_staging):$(staging_project_root)/media/pdf/* $(live_project_root)/media/pdf/')
    
    # sync fixture
    push_fixture('bailout_pdfs', restart_server=True)
    
def push_flatpages():
    "Pushes data from the flatpages application from staging to production"
    subsidyscope_setup()
    push_fixture('flatpages', restart_server=True)

# def push_tarp():
#     "Pushes files and fixtures supporting the bailout application (TARP database) from staging to production."
#     # setup -- all commands go through a shell connection to the live site
#     subsidyscope_setup()
#     # sync TARP data
#     push_fixture('etl', restart_server=False)
#     push_fixture('bailout', restart_server=True)
# 
# def push_local_fixture_to_staging(fixture_name=None, restart_server=False):
#     """ Dumps local data and loads it onto the staging server """
#     "Moves the specified fixture from staging to production"
#     if fixture_name is None:
#         prompt('app_name', 'What application fixture would you like to push from your local server to staging?')
#         fixture_name = ENV['app_name']
#     
#     # generate, transfer and sync fixture
#     set(fixture=fixture_name)
#     local('python $(local_project_root)/manage.py dumpdata $(fixture) > $(local_project_root)/data/$(fixture).json')
#     local('scp -C -i $(local_project_root)/data/$(fixture).json $(subsidyscope_local_ssh_keyfile_for_staging) $(subsidyscope_local_login_for_staging):$(staging_project_root)')
#     run('export PYTHONPATH=$(staging_python_root):$PYTHONPATH && python $(staging_project_root)/manage.py loaddata $(staging_project_root)/data/$(fixture).json')
# 
# 
#     run('ssh -i $(live_ssh_keyfile_for_staging) $(live_login_for_staging) "export PYTHONPATH=$(staging_python_root):$PYTHONPATH && python $(staging_project_root)/manage.py dumpdata $(fixture) > $(staging_project_root)/data/$(fixture).json"')
#     run('scp -C -i $(live_ssh_keyfile_for_staging) $(live_login_for_staging):$(staging_project_root)/data/$(fixture).json $(live_project_root)/data/$(fixture).json')
# 
#     
#     if restart_server is True:
#         run('/home/subsidyscope/run-this.sh')    

def push_local_tarp_to_staging():
    """ Pushes local etl and bailout fixtures up to staging server """
    subsidyscope_setup()
    push_local_fixture_to_staging('etl', restart_server=False)
    push_local_fixture_to_staging('bailout', restart_server=True)
     
def push_project_updates():
    "Pushes files and fixtures supporting the project_updates application (mini-blog) from staging to production."
    # setup -- all commands go through a shell connection to the live site
    subsidyscope_setup()
    
    # sync images
    run('rsync -r -v -z --exclude=".*" -e "ssh -i $(live_ssh_keyfile_for_staging)" $(live_login_for_staging):$(staging_project_root)/media/images/project_update_* $(live_project_root)/media/images/')
    
    # sync project update data
    push_fixture('project_updates', restart_server=True)
    

def drop_and_reload_live_models(app=None):
    subsidyscope_setup()
    
    if app is None:
        print 'WARNING: executing this process will completely remove the relevant application\'s data from the live server before reloading it. If something goes wrong, it could go *really* wrong.'
        print 'The process is as follows:'
        print '  1. drop application tables'
        print '  2. SVN up the application'
        print '  3. create application tables'
        print '  4. push application fixture from data.subsidyscope.com to live'
        confirmation = raw_input('Are you sure you wish to proceed? (yes/no): ')
    else:
        confirmation = 'yes'
        ENV['app_name'] = app
        
    if confirmation=='yes':        
        if app is None:
            prompt('app_name', 'What application should we refresh?')        

        # grab database settings
        download('$(live_project_root)/local_settings.py', 'local_settings.py')
        local('mv local_settings.py.subsidyscope.com subsidyscope_com_local_settings.py')
        import subsidyscope_com_local_settings
        assert subsidyscope_com_local_settings.DATABASE_ENGINE=='mysql', "live site appears to not be using mysql"

        db_settings = []
        if subsidyscope_com_local_settings.DATABASE_USER:
            db_settings.append('-u%s' % subsidyscope_com_local_settings.DATABASE_USER)
        if subsidyscope_com_local_settings.DATABASE_PORT:
            db_settings.append('-P%s' % subsidyscope_com_local_settings.DATABASE_PORT)
        if subsidyscope_com_local_settings.DATABASE_PASSWORD:
            db_settings.append('-p%s' % subsidyscope_com_local_settings.DATABASE_PASSWORD)
        if subsidyscope_com_local_settings.DATABASE_HOST:
            db_settings.append('-h%s' % subsidyscope_com_local_settings.DATABASE_HOST)            
        if subsidyscope_com_local_settings.DATABASE_NAME:
            db_settings.append('-D%s' % subsidyscope_com_local_settings.DATABASE_NAME)

        set(mysql = ('mysql %s' % (' '.join(db_settings))))        

        # DROP
        run('python $(live_project_root)/manage.py sqlclear $(app_name) | $(mysql)')

        # SVN up
        run('svn up $(live_project_root)/$(app_name)/models.py $(live_project_root)/$(app_name)/admin.py')
        
        # CREATE
        run('python $(live_project_root)/manage.py sql $(app_name) | $(mysql)')

        # PUSH DATA
        push_fixture(ENV['app_name'])

def launch_the_damn_thing():
    subsidyscope_setup()
         
    run('svn up $(live_project_root)')
    run('python $(live_project_root)/manage.py syncdb') # handle new app for gchart stuff
    push_fixture('tarp_subsidy_graphics')
    drop_and_reload_live_models('bailout')
    drop_and_reload_live_models('project_updates')
    
