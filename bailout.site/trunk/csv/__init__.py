import os, csv
from django.conf import settings
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
            imp.find_module('csv', app_path)
        except ImportError:
            continue
        
        __import__("%s.csv" % app)


class CSVFile():
    
    def __init__(self, model):
        self.model = model 
    
    def generate_data(self):         
        
        writer = csv.writer(response)
        
        writer.writerow(map(lambda x: x[0], self.fields))
    
        items = self.model.objects.select_related()
        
        if self.order_by:
            items.order_by(self.order_by)
        
        for item in items:
    
            record = []
            for f in self.fields:
                temp = t
                for p in fields[f[1]].split('.'):
                    temp = getattr(temp, p)
                    if callable(temp):
                        temp = temp()
                        
                record.append(temp)
    
            writer.writerow(record)
    
        return response
            
class CSVManager():
    
    def __init__(self):
        self._registry = {}
    
    def register(self, model, csv_class=None):

        if not csv_class:
            csv_class = CSVFile
        
        if not isinstance(model, ModelBase):
            raise AttributeError('The model being registered must derive from Model.')
        
        if model in self._registry:
            raise AlreadyRegistered('The model %s is already registered' % model.__class__)
        
        self._registry[model] = csv_class(model)
    
    
manager = CSVManager()