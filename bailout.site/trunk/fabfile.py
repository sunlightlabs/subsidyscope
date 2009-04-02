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


# DEPRECATED FOR DATA-HEAVY APPLICATIONS
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


# DEPRECATED FOR DATA-HEAVY APPLICATIONS
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
    

def get_mysql_string(subsidyscope_com_local_settings):
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
    return 'mysql %s' % ' '.join(db_settings)

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
        set(mysql = get_live_mysql_string())

        # DROP
        run('python $(live_project_root)/manage.py sqlclear $(app_name) | $(mysql)')

        # SVN up
        run('svn up $(live_project_root)/$(app_name)/models.py $(live_project_root)/$(app_name)/admin.py')
        
        # CREATE
        run('python $(live_project_root)/manage.py sql $(app_name) | $(mysql)')

        # PUSH DATA
        push_fixture(ENV['app_name'])

def get_staging_mysql_string():
    """ returns mysql string for staging server """
    subsidyscope_setup()    
    local('scp -C -i $(subsidyscope_local_ssh_keyfile_for_staging) $(subsidyscope_local_login_for_staging):$(staging_project_root)/local_settings.py $(local_project_root)/local_settings_staging.py')
    import local_settings_staging
    assert local_settings_staging.DATABASE_ENGINE=='mysql', "staging site appears not to be using mysql"
    local('rm $(local_project_root)/local_settings_staging.py')
    return get_mysql_string(local_settings_staging)
    
    
def get_local_mysql_string():
    """ returns mysql string for local server """
    import local_settings
    assert local_settings.DATABASE_ENGINE=='mysql', "local site appears not to be using mysql"
    return get_mysql_string(local_settings)


def get_live_mysql_string():
    """ returns mysql string for local server """
    subsidyscope_setup()    
    download('$(live_project_root)/local_settings.py', 'local_settings.py')
    local('mv local_settings.py.subsidyscope.com local_settings_live.py')
    import local_settings_live
    assert local_settings_live.DATABASE_ENGINE=='mysql', "live site appears not to be using mysql"
    local('rm local_settings_live.py')
    return get_mysql_string(local_settings_live)


def convert_mysql_string_to_mysqldump(m):
    """ converts a mysql string to a mysqldump string; assumes -D flag comes last """
    return m.replace('mysql ', 'mysqldump ').replace('-D', '')

def get_staging_table_names(fixture_name):
    # figure out which tables are involved in the app
    # (need to write to a file because fabric doesn't capture output of local())
    set(app_name=fixture_name)
    re_create_table = re.compile(r'CREATE\s*TABLE\s*`?(.*?)`?\s*[\($]', re.I)
    subsidyscope_setup()
    tables = []
    local('python $(local_project_root)/manage.py sql $(app_name) > /tmp/$(app_name)-create.sql')
    f = open('/tmp/%s-create.sql' % ENV['app_name'],'r')
    create_sql = f.readlines()
    f.close()
    local('rm /tmp/$(app_name)-create.sql')    
    for line in create_sql:
        m = re_create_table.search(line)
        if m:
            tables.append(m.group(1))
    return tables

def push_fixture_from_local_to_staging_via_mysql(fixture_name=None, backup=True):
    """ push fixture from local to staging using SQL instead of fixtures (as fixtures have turned flaky) """
    if fixture_name is None:
        prompt('app_name', 'What application fixture would you like to move from local to staging?')
        fixture_name = ENV['app_name']

    set(app_name=fixture_name)

    # backup DB
    if backup:
        local('ssh -i $(subsidyscope_local_ssh_keyfile_for_staging) $(subsidyscope_local_login_for_staging) "~/subsidyscope_backup.sh"')

    tables = get_staging_table_names(fixture_name)
    
    # dump the tables to a local file
    mysqldump = '%s %s > /tmp/$(app_name).sql' % (convert_mysql_string_to_mysqldump(get_local_mysql_string()), ' '.join(tables))
    local(mysqldump)
    
    # copy dumped file to staging server
    local('scp -C -i $(subsidyscope_local_ssh_keyfile_for_staging) /tmp/$(app_name).sql $(subsidyscope_local_login_for_staging):$(staging_project_root)/data/ && rm /tmp/$(app_name).sql')

    # import file contents on staging server and delete it
    staging_mysql = get_staging_mysql_string()
    local('ssh -i $(subsidyscope_local_ssh_keyfile_for_staging) $(subsidyscope_local_login_for_staging) "cat $(staging_project_root)/data/$(app_name).sql | %s && ~/run-this.sh && rm $(staging_project_root)/data/$(app_name).sql"' % staging_mysql)
    

def push_fixture_from_staging_to_live_via_mysql(fixture_name=None, backup=True):
    """ push the TARP tables from staging to live using SQL instead of fixtures (as fixtures have turned flaky) """
    if fixture_name is None:
        prompt('app_name', 'What application fixture would you like to move from staging to production?')
        fixture_name = ENV['app_name']
        
    set(app_name=fixture_name)

    # backup DB
    if backup:
        run('~/subsidyscope_backup.sh')

    # use staging to figure out which tables are included in the app
    tables = get_staging_table_names(fixture_name)

    # dump the tables into a file on staging
    mysqldump = '%s %s' % (convert_mysql_string_to_mysqldump(get_staging_mysql_string()), ' '.join(tables))
    run('ssh -i $(live_ssh_keyfile_for_staging) $(live_login_for_staging) "%s > /tmp/$(app_name).sql"' % mysqldump)

    # copy the file onto the production server
    run('scp -C -i $(live_ssh_keyfile_for_staging) $(live_login_for_staging):/tmp/$(app_name).sql /tmp/$(app_name).sql')

    # delete the file from the staging server
    run('ssh -i $(live_ssh_keyfile_for_staging) $(live_login_for_staging) "rm /tmp/$(app_name).sql"')

    # import the sqldump on the live server
    live_mysql = get_live_mysql_string()
    run('cat /tmp/$(app_name).sql | %s && ~/run-this.sh && rm /tmp/$(app_name).sql' % live_mysql)
    
    
def push_local_imported_tarp():
    """ pushes locally-imported TARP changes to the staging server """
    subsidyscope_setup()
    push_fixture_from_local_to_staging_via_mysql('etl')
    push_fixture_from_local_to_staging_via_mysql('bailout', backup=False) # only backup before the first operation so we can roll back properly

def push_tarp():
    """ pushes bailout fixture from staging to production """
    subsidyscope_setup()
    push_fixture_from_staging_to_live_via_mysql('etl')
    push_fixture_from_staging_to_live_via_mysql('bailout', backup=False) # only backup before the first operation so we can roll back properly
