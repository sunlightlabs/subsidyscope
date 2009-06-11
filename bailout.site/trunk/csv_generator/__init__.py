import os, csv, time
from django.conf import settings
from django.db.models.base import ModelBase
from django.core.exceptions import ImproperlyConfigured

def autodiscover():

    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
    
        try:
            app_path = __import__(app, {}, {}, [app.split('.')[-1]]).__path__
        except AttributeError:
            continue

        try:
            imp.find_module('csv_def', app_path)
        except ImportError:
            continue
        
        __import__("%s.csv_def" % app)


class CSVFile():
    
    app_name = None
    filename = None
    model = None
    
    def __init__(self, model):
        self.model = model 
    
    def generate_metadata(self):     
    
        if self.app_name == None:
            self.app_name = self.model._meta.app_label
        
        filename = self.filename + '_metadata.txt'
        csv_filename = self.filename + '.csv'
        
        print 'Generating CSV metadata for %s: %s' % (self.app_name, filename)
        
        output_path = os.path.join(settings.CSV_OUTPUT_PATH, self.app_name)
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        output_file_path = os.path.join(output_path, filename) 
        
        if os.path.exists(output_file_path):
            os.remove(output_file_path)
        
        metadata_file = open(output_file_path, 'w')
        
        metadata_file.write('Metadata for %s\n' % (csv_filename))
        metadata_file.write('Generated on %s\n' % (time.strftime('%b %d, %Y')))
        
        metadata_file.write('\n\nFile Description: %s\n' % (self.description))
        
        metadata_file.write('\n\nField Descriptions:\n\n')
        
        
        for f in self.fields:
            metadata_file.write('\t%s\n\t%s\n\n' % (f[0], f[2]))
        
        metadata_file.close()
        
        
        
        
    def generate_data(self):         
        
        if self.app_name == None:
            self.app_name = self.model._meta.app_label
        
        filename = self.filename + '.csv'
        
        print 'Generating CSV for %s: %s' % (self.app_name, filename)
        
        output_path = os.path.join(settings.CSV_OUTPUT_PATH, self.app_name)
        
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        output_file_path = os.path.join(output_path, filename) 
        
        if os.path.exists(output_file_path):
            os.remove(output_file_path)
        
        csv_file = open(output_file_path, 'wb')
        
        writer = csv.writer(csv_file)
        
        writer.writerow(map(lambda x: x[0], self.fields))
    
        items = self.model.objects.select_related()
        
        if self.order_by:
            items.order_by(self.order_by)
        
        for item in items:
    
            record = []
            for f in self.fields:
                temp = item
                for p in f[1].split('.'):
                    temp = getattr(temp, p)
                    if callable(temp):
                        temp = temp()
                    
                    if len(f) == 4 and temp:
                        temp = f[3](temp)
                        
                record.append(temp)
    
            writer.writerow(record)

        csv_file.close()
        
        
            
class CSVManager():
    
    def __init__(self):
        self._registry = {}
    
    def register(self, model, csv_class=None):

        if not csv_class:
            csv_class = CSVFile
        
        #if not isinstance(model, ModelBase):
        #    raise AttributeError('The model being registered must derive from Model.')
        
        #if model in self._registry:
        #    raise AlreadyRegistered('The model %s is already registered' % model.__class__)
        
        self._registry[model] = csv_class(model)
        
    def generate_data(self):
        
        for model in self._registry:
            csv_file = self._registry[model]
            csv_file.generate_data()
            csv_file.generate_metadata()
    
    def generate_metadata(self):
        
        for model in self._registry:
            csv_file = self._registry[model]
            csv_file.generate_metadata()
    
    
manager = CSVManager()