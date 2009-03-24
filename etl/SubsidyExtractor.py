import sys, os, types, re
import OpenAnything
from django.db import models
from etl.models import DataSource, DataRun
from bailout.models import Institution, Transaction

# import based on path without permanently affecting PYTHONPATH
def import_by_path(path,module):
    sys.path.insert(0,path)
    m = __import__(module)
    del sys.path[0]
    return m
    

class SubsidyExtractor:
    """Pluggable framework for extracting from data sources"""
    def __init__(self, directory=None, identifier=None):
        if identifier:
            self._identifier = identifier
        else:
            self._identifier = self.__module__

        if directory:
            self._data_directory = '%s/data' % re.compile('\/\s*$').sub('',directory.strip())
            if not os.path.exists(self._data_directory):
                os.mkdir(self._data_directory) 
        
        # dict of the most recently retrieved files
        self._retrieved_files = {}
        
        # current data run
        self._datarun = None
        
        # bookkeeping
        self._records_inserted = 0
        self._records_updated = 0      
      
    def ready(self):
        """Returns true or false -- should an import run be undertaken at this time?"""
        # TODO: convenience function to check if it's been X hours (or whatever) since last run
        return False
      
    def get_data(self):
        """Retrieve and store the source data, but do not process them. For example: download but do not parse PDFs; download and gzip but do not parse CSVs."""
        source, source_was_created = DataSource.objects.get_or_create(name=self._identifier)            
        self._datarun = DataRun.objects.create(source=source)
                      
    def process_data(self):
        pass
        
    def _record_stats(self):
        """Updates Django data run-tracking system with information on what's just been done -- number of records inserted, errors encountered, etc."""
        self._datarun.records_inserted = self._records_inserted
        self._datarun.records_updated = self._records_updated
        self._datarun.save()
        
    def make_absolute_url(self, absolute_source_url, url):
        """Convert a relative URL to an absolute URL (if necessary)
        
        >>> q = SubsidyExtractor()
        
        >>> q.make_absolute_url('http://www.google.com/abc','/toc/index.html')
        'http://www.google.com/toc/index.html'
        
        >>> q.make_absolute_url('http://www.google.com/abc/','/toc/index.html')
        'http://www.google.com/toc/index.html'
        
        >>> q.make_absolute_url('http://www.google.com/abc/','toc/index.html')
        'http://www.google.com/abc/toc/index.html'
        
        >>> q.make_absolute_url('http://www.google.com/abc','toc/index.html')
        'http://www.google.com/toc/index.html'
        
        >>> q.make_absolute_url('http://www.google.com','toc/index.html')
        'http://www.google.com/toc/index.html'
        
        >>> q.make_absolute_url('http://www.google.com','/toc/index.html')
        'http://www.google.com/toc/index.html'
        
        >>> q.make_absolute_url('http://www.google.com/','toc/index.html')
        'http://www.google.com/toc/index.html'
        
        >>> q.make_absolute_url('http://www.google.com/','/toc/index.html')
        'http://www.google.com/toc/index.html'
        """
        
        if url.startswith('http://'):
            return url
        else:
            if url.startswith('/'):
                # chop off the end of the source URL
                return re.compile('(http:\/\/[^\/]+)\/.*$').sub('\g<1>',absolute_source_url) + url
            else:
                # add a final slash, if only the domain name has been specified
                if re.compile('http:\/\/[^\/]+$').match(absolute_source_url):
                    absolute_source_url = absolute_source_url + '/'
                    
                # chop off the end of the source URL
                return re.compile('([^\/])\/[^\/]+$').sub('\g<1>/',absolute_source_url) + url
    

    # TODO: add versioning to data retrieval -- should come from Django data run architecture
    def retrieve_and_store_files(self, parent_url, links):
        """Fetch a list of hrefs -- which may be absolute, relative, or URLs -- and store them in a predictable filesystem structure, with etag support. Names of retrieved files are stored in a dict that maps input links to their new locations filenames."""

        # reset internal dict of retrieved files
        self._retrieved_files = {}
        
        # compile regexes
        re_sanitize_filename = re.compile('[^\.\/\-_a-z0-9]',re.I)
        re_strip_filename = re.compile('\/[^\/]*$')
        re_remove_double_slashes = re.compile('\/{2,}')
        
        # iterate through input links
        for link in links:
            
            # clean strings, transform to URLs
            url = self.make_absolute_url(parent_url,link)
            document_filename = re_remove_double_slashes.sub('/','%s/%s' % (self._data_directory, re_sanitize_filename.sub('_',link)))
            etag_filename = '%s.etag' % document_filename
        
            # create storage directory if it doesn't exist
            document_storage_dir = re_strip_filename.sub('',document_filename)
            if not os.path.exists(document_storage_dir):
                os.makedirs(document_storage_dir)    
            
            # get etag of file if it's known (from previous run)
            etag = None            
            if os.path.exists(etag_filename):
                etag_file = open(etag_filename,'r')
                etag = etag_file.read().replace("\"","")
                etag_file.close()

            # fetch file, store data
            current_document = OpenAnything.fetch(url, etag=etag)
            document_file = open(document_filename,'w')
            document_file.write(current_document['data'])
            document_file.close()

            self._retrieved_files[link] = document_filename

            # store etag
            if not current_document['etag'] is None:
                etag_file = open(etag_filename,'w')
                etag_file.write(current_document['etag'])
                etag_file.close()
         
        # not strictly necessary, but might be useful in some circumstances      
        return self._retrieved_files
    
    def get_pdf_contents(self,file_path):
        """ retrieve the contents of a PDF as lines of text using the pdftotext utility
        
        >>> # check that pdftotext exists and is in the path
        >>> import os        
        >>> f = os.popen("which pdftotext | wc -l") 
        >>> int(f.read().strip())>0
        True
        
        >>> # run a simple test PDF
        >>> q = SubsidyExtractor()
        >>> lines = q.get_pdf_contents(os.path.abspath(os.path.dirname(sys.argv[0])) + '/tests/simple.pdf')
        >>> lines[0].strip()
        'The quick'
        >>> lines[1].strip()
        'brown fox'
        >>> lines[2].strip()
        'jumped over'
        >>> lines[3].strip()
        'the lazy dog.'
        """
        
        f = os.popen("pdftotext -layout -q %s - 2>/dev/null" % file_path)
        r = f.readlines()
        f.close()
        return r
        
    # def get_pdf_date(self,file_path):
    #     """ retrieves the date of the, giving preference to modified, then creation 
    #     
    #      >>> # check that pdfinfo exists and is in the path
    #     >>> import os        
    #     >>> f = os.popen("which pdftotext | wc -l") 
    #     >>> int(f.read().strip())>0
    #     True
    #     
    #     >>> # run a simple test PDF
    #     >>> q = SubsidyExtractor()
    #     >>> lines = q.get_pdf_modified_date(os.path.abspath(os.path.dirname(sys.argv[0])) + '/tests/simple.pdf')        
    #     (2010, 1, 1, 11, 46, 54, 4, 9, 0)
    #     """
    #     
    #     re_creation_date = re.compile('^CreationDate:\s+(.*?)$')
    #     re_modification_date = re.compile('^ModDate:\s+(.*?)$')
    #     
    #     parsedate = pdt.Calendar()
    #     f = os.popen("pdfinfo %s - 2>/dev/null" % file_path)
    #     output = f.readlines()
    #     f.close()
    # 
    #     for l in output:
    #         m = re_modification_date.match(l)
    #         if m!=None:
    #              return pdt.parseDateText(m.group(1))
    #         
    #          m = re_creation_date.match(l)
    #          if m!=None:
    #               return pdt.parseDateText(m.group(1))
    #     
    #     return None

def main(importer_name):
    # find sources and import
    
    # determine location
    path = os.path.abspath(os.path.dirname(sys.argv[0]))

    # find sources -- they will be named like {data-extractor}/{data-extractor}.py
    for modulename in os.listdir(path):
        
        if importer_name=='all' or modulename==importer_name:
        
            moduledir = '%s/%s' % (path,modulename)
            modulepath = '%s/%s.py' % (moduledir, modulename)
            if os.path.isdir(moduledir) and os.path.exists(modulepath):

                # import the module
                subextractor = import_by_path(moduledir,modulename)

                # look at its classes, determine which ones are inherited from SubsidyExtractor
                for candidate in dir(subextractor):
                    ref = getattr(subextractor,candidate)
                    if type(ref)==types.ClassType and hasattr(subextractor, 'SubsidyExtractor') and issubclass(ref,subextractor.SubsidyExtractor.SubsidyExtractor):
                        current_extractor = ref(directory=moduledir)
                    
                        # TODO: catch errors on ready(); do logging of run
                        if current_extractor.ready():
                        
                            # TODO: these functions are split to allow for future forking of the download phase for speediness's sake
                            # TODO: try..catch block surrounding these guys?
                            current_extractor.get_data()
                            current_extractor.process_data()              
     
     
def show_help():
    """Prints simple usage information."""
    pass
                
if __name__=='__main__':   

    did_something = False

    if len(sys.argv)==2:
        if sys.argv[1]=='test':
            did_something = True
            import doctest
            doctest.testmod()        
                
    if len(sys.argv)==3:
        if sys.argv[1]=='run':  
            did_something = True         
            main(sys.argv[2])
            
    if not did_something:
        show_help()

    

# # useful exception catchall?
# try:
#     <Exception generating code>
# except Exception, e:
#     print '%s: %s' % (e.__class__.__name__, e)
#     if isinstance(e, SystemExit): 
#         raise # take the exit
#     except:
#         print 'Nonstandard Exception %r: %r' % __import__('sys').exc_info()[:2]