import settings
import zlib
import base64
import urllib
import pickle
from decimal import Decimal
from hashlib import md5 
from pysolr import Solr
from base64 import urlsafe_b64encode, urlsafe_b64decode
from django.db import models
from django import forms
from haystack.query import SearchQuerySet
import django.db.models.fields
from django.core.cache import cache
from sectors.models import *
from faads.models import SearchHash
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.humanize.templatetags.humanize import intcomma


def uri_b64encode(s):
   return urlsafe_b64encode(s).strip('=')


def uri_b64decode(s):
   return urlsafe_b64decode(s + '=' * (4 - len(s) % 4))


def compress_querydict(obj):
    querydict = uri_b64encode(zlib.compress(pickle.dumps(obj)))
    search_hash = md5(querydict).hexdigest()
    (h, created) = SearchHash.objects.get_or_create(search_hash=search_hash, defaults={'querydict': querydict})
    return h.search_hash


def decompress_querydict(s):
    h = get_object_or_404(SearchHash, search_hash=s)
    return pickle.loads(zlib.decompress(uri_b64decode(str(h.querydict))))


def get_sector_by_name(sector_name=None):
    sector = None
    if sector_name is not None:
        sector = Sector.objects.filter(name__icontains=sector_name)
        if len(sector)==1:
            sector = sector[0]
        else:
            sector = None

    return sector


class USASpendingSearchBase():

    SOLR_MAX_RECORDS = 1200000    

    SOLR_USE_STATS_MODULE = getattr(settings, 'HAYSTACK_SOLR_STATS_MODULE_ENABLED', False)    
    
    CONJUNCTION_AND = {'solr': 'AND', 'mysql': 'AND'}
    CONJUNCTION_OR = {'solr': 'OR', 'mysql': 'OR'}
    
    
    def __init__(self, query_string=None):
        
        self.filters = []
        self.sectors = []
        
        self.aggregate_by = None
        self.use_solr = False
        self.order_by = None
        self.cache = True
        self.SearchQuerySet = None
        
        self.field_objects = {}
        for field in self.DJANGO_MODEL._meta.fields:
            self.field_objects[field.name] = field
            

    def __len__(self):
        return self.count()

    
    # clone function to enable chainable filtering (blatantly stolen from haystack (which presumably stole it from Django))
    def _clone(self, klass=None):

        if klass is None:
            klass = self.__class__

        clone = klass()
        clone.aggregate_by = self.aggregate_by
        clone.use_solr = self.use_solr
        clone.order_by = self.order_by
        clone.cache = self.cache
        clone.sectors = self.sectors[:]
        clone.field_objects = self.field_objects.copy()
        clone.filters = self.filters[:]
        if self.SearchQuerySet is not None:
            clone.SearchQuerySet = self.SearchQuerySet._clone()
        
        return clone
    
    def set_sectors(self, s=None):
        if s is None:
            return self

        # accept sector or list of sectors
        if type(s) not in (list, tuple):
            s = [s]

        clone = self._clone()
        clone.sectors = s
        return clone
        
    def use_cache(self, u=True):
        clone = self._clone()
        clone.cache = u
        return clone
            
    def get_query_cache_key(self, aggregate_by=''):
        fs = "%s;" % self.__module__
        for i,f in enumerate(self.filters):
            fs += "%d:{%s|%s|%s}" % (i, str(f[0]), str(f[1]), str(f[2]))
        fs += aggregate_by
        h = md5(fs).hexdigest() # avoid key length problems
        return str(h)
                    
    def filter(self, filter_by, filter_value, filter_conjunction=CONJUNCTION_AND):  

        field_lookup = self.FIELD_MAPPINGS.get(filter_by,None)
        if field_lookup is None:
            raise Exception("'%s' is not a valid filter field" % filter_by)
        elif type(filter_value) is int and field_lookup['type']=='fk':
            filter_value = (filter_value,)
        elif len(filter_value)==0:
                if field_lookup['type']=='fk':
                    filter_value = (-1,) # plan to return an empty result set if this criteria is an empty query on an FK field
                else:
                    raise Exception("Cannot process a zero-length value for filter '%s'" % filter_by)            
        elif field_lookup['type']=='range' and ((type(filter_value) not in (list, tuple)) or (len(filter_value)!=2)):
            raise Exception("'%s' is a ranged field. Please pass a tuple or list of length 2 (None==wildcard)" % filter_by)

        clone = self._clone()

        # invalidate existing queryset, if any
        self.SearchQuerySet = None        

        clone.filters.append( (filter_by, filter_value, filter_conjunction) )
        if not clone.use_solr and (clone.FIELD_MAPPINGS[filter_by]['type']=='text'):
            clone.use_solr = True
            
        return clone
    
    def _build_solr_query(self):
        query = ''
        
        if len(self.sectors):
            query += "(%s:(%s)) AND " % (self.FIELD_MAPPINGS['sectors']['solr_field'], " OR ".join(map(lambda x: str(x.id), self.sectors)))        
        
        for i,f in enumerate(self.filters):
            filter_field = f[0]
            filter_value = f[1]
            filter_conjunction = f[2]
            
            if i>0:
                query += " %s " % filter_conjunction['solr'] 


            # deal with queries against foreign key fields
            if self.FIELD_MAPPINGS[filter_field]['type']=='fk':
                fk_transformation = self.FIELD_MAPPINGS[filter_field].get('solr_transformation', lambda x: x)

                if type(filter_value) not in (list, tuple):
                    filter_value = (filter_value,)
                
                fk_values = []
                for value in filter_value:
                    fk_value = fk_transformation(value)                    
                    if fk_value is not None:
                        fk_values.append(str(fk_value))
                
                if len(fk_values):                
                    query += '(%s:(%s))' % (self.FIELD_MAPPINGS[filter_field]['solr_field'], ' OR '.join(fk_values))


            # deal with range-type queries 
            elif self.FIELD_MAPPINGS[filter_field]['type']=='range':
                clause_parts = []
                range_transformation = self.FIELD_MAPPINGS[filter_field].get('solr_transformation', lambda x: x) # putting this in place to allow for varying formatting of dates for solr & mysql
                
                for range_specifier in filter_value:
                    if range_specifier is None:
                        clause_parts.append('*')
                    else:
                        clause_parts.append(str(range_transformation(range_specifier)))
                        
                query += '(%s:[%s])' % (self.FIELD_MAPPINGS[filter_field]['solr_field'], ' TO '.join(clause_parts))

            # text queries (all of which get sent to solr)
            elif self.FIELD_MAPPINGS[filter_field]['type']=='text':
                query += '(%s:"%s")' % (self.FIELD_MAPPINGS[filter_field]['solr_field'], filter_value)
        
        query = "(django_ct:%s.%s) AND (%s)" % (self.DJANGO_MODEL._meta.app_label, self.DJANGO_MODEL._meta.module_name, query)
        
        return query

    
    def _build_sector_bitmask(self):
        m = 0
        for s in self.sectors:
            m = m | s.binary_hash()
        return m
        
    def _build_mysql_query(self, aggregation_override=False):
        
        if not aggregation_override:      
            if self.aggregate_by is None:
                raise Exception("Must specify an aggregate field prior to MySQL query construction")

            if self.aggregate_by == self.FIELD_MAPPINGS['fiscal_year']:
                # an exception to the field naming rule...
                aggregate_field = self.aggregate_by['mysql_field']
            else:
                # otherwise append id to all foreign key fields to match db schema
                aggregate_field = self.aggregate_by['mysql_field'] + '_id'

        sql_parameters = [] # uses proper django.db SQL-escaping, in case we ever introduce nonnumeric database queries for some reason
        
        sql = " SELECT %s as field, sum(%s) as value FROM %s " % (aggregation_override and aggregation_override or aggregate_field, self.FIELD_MAPPINGS[self.FIELD_TO_SUM]['mysql_field'], self.DJANGO_MODEL._meta.db_table)
        
        if (len(self.filters) + len(self.sectors)) > 0:
            
            sql += " WHERE "

            if len(self.sectors):
                sql += '(%s & %d)' % (self.FIELD_MAPPINGS['sectors']['mysql_field'], self._build_sector_bitmask())
                if len(self.filters):
                    sql += " AND "
        
            for i,f in enumerate(self.filters):
                
                filter_field = f[0]
                filter_value = f[1]
                filter_conjunction = f[2]
    
                # add conjunction if this isn't the first part of the clause
                if i>0:
                    sql += " %s " % filter_conjunction['mysql']
                
                # deal with queries against foreign key fields (there are many of them!)
                if self.FIELD_MAPPINGS[filter_field]['type']=='fk':
                    
                    # build list of the foreign keys
                    fk_transformation = self.FIELD_MAPPINGS[filter_field].get('mysql_transformation', lambda x: x)
    
                    if type(filter_value) not in (list, tuple):
                        filter_value = (filter_value,)
                    
                    fk_values = []
                    for value in filter_value:
                        fk_value = fk_transformation(value)
                        if fk_value is not None:
                            fk_values.append(str(fk_value))
                    
                    # is this query examining a field that's an aggregation of two fields in solr? if so, it doesn't exist in mysql. build
                    # an OR clause instead
                    mysql_field = self.FIELD_MAPPINGS[filter_field]['mysql_field']               
                    if type(mysql_field) not in (list, tuple):
                        mysql_field = (mysql_field,)            
                    
                    clauses = []
                    for mf in mysql_field:
                        clauses.append(' (%s_id IN (%s)) ' % (mf, ','.join(fk_values)))                        
                    
                    sql += '(' + ' OR '.join(clauses) + ')'
                   
                # deal with range-type queries 
                elif self.FIELD_MAPPINGS[filter_field]['type']=='range':
                    # okay, I admit this may be too cute for its own good. the goal is just to build '( date>%s AND date<%s )' with options for leaving either off via None
                    clause_parts = []
                    range_transformation = self.FIELD_MAPPINGS[filter_field].get('mysql_transformation', lambda x: x) # putting this in place to allow for varying formatting of dates for solr & mysql
                    range_comparators = ('>=', '<=')
                    for j, range_specifier in enumerate(filter_value):
                        if range_specifier is not None:
                            clause_parts.append(self.FIELD_MAPPINGS[filter_field]['mysql_field'] + range_comparators[j] + "%s")
                            sql_parameters.append(range_transformation(range_specifier))
                    sql += ' ( %s ) ' % (' AND '.join(clause_parts))

        sql += " GROUP BY %s " % (aggregation_override and aggregation_override or aggregate_field)

        return (sql, sql_parameters)
        
    
    def aggregate(self, aggregate_by=None):
        
        if aggregate_by is None:
            aggregate_by = self.DEFAULT_AGGREGATION_FIELD
        
        # ensure that aggregation is to be performed along an acceptable dimension
        self.aggregate_by = self.FIELD_MAPPINGS.get(aggregate_by, None)
        if self.aggregate_by is None:
            raise Exception("Cannot aggregate by %s - not a valid field" % aggregate_by)
        elif not self.aggregate_by.get('aggregate', False):
            raise Exception("Cannot aggregate by %s - incompatible field type" % aggregate_by)
        
        # check for cached result
        if self.cache:
            cached_result = cache.get(self.get_query_cache_key(aggregate_by=aggregate_by))            
            if cached_result is not None:
                return cached_result
    
        # handling full-text aggregation with solr/python hack
        if self.use_solr:                        
            
            solr = Solr(settings.HAYSTACK_SOLR_URL)
            query = self._build_solr_query()
            search_fields = { 
                'q': query,
                'rows': self.SOLR_MAX_RECORDS,
                'fl': '%s,%s' % (self.FIELD_MAPPINGS[self.FIELD_TO_SUM]['solr_field'], self.FIELD_MAPPINGS[aggregate_by]['solr_field']),
                'facet': 'true',
                'facet.field': self.FIELD_MAPPINGS[aggregate_by]['solr_field'],
            }
            if self.SOLR_USE_STATS_MODULE:
                search_fields['rows'] = 0
                search_fields['stats'] = 'true'
                search_fields['stats.field'] = self.FIELD_MAPPINGS[self.FIELD_TO_SUM]['solr_field']
                search_fields['stats.facet'] =self.FIELD_MAPPINGS[aggregate_by]['solr_field']
                
            solr_result = solr.search(**search_fields)
            result = {}
            
            # aggregation
            
            # can we use the solr stats module?
            if self.SOLR_USE_STATS_MODULE:

                if solr_result.stats['stats_fields'][self.FIELD_MAPPINGS[self.FIELD_TO_SUM]['solr_field']] is not None:                    
                    for (year, stats) in solr_result.stats['stats_fields'][self.FIELD_MAPPINGS[self.FIELD_TO_SUM]['solr_field']]['facets'][self.FIELD_MAPPINGS[aggregate_by]['solr_field']].items():
                        result[int(year)] = Decimal(str(stats['sum']))
                
            # if not: painful, slow aggregation
            else:            
                for doc in solr_result.docs:
                    if doc.has_key(self.FIELD_MAPPINGS[aggregate_by]['solr_field']) and doc.has_key(self.FIELD_MAPPINGS[self.FIELD_TO_SUM]['solr_field']):
                        key = int(doc[self.FIELD_MAPPINGS[aggregate_by]['solr_field']])    
                        if not result.has_key(key):
                            result[key] = Decimal(0)                
                        result[key] += Decimal(str(doc[self.FIELD_MAPPINGS[self.FIELD_TO_SUM]['solr_field']])) 
            
        
        # handling key based aggregation with db group by/sum
        else:
            
            from django.db import connection
            cursor = connection.cursor()                
            
            sql, sql_parameters = self._build_mysql_query()

            cursor.execute(sql, sql_parameters)
            
            result = {}            
            for row in cursor.fetchall():
                result[row[0]] = row[1]
    
        cache.set(self.get_query_cache_key(aggregate_by=aggregate_by), result)
    
        return result    
    
    
    def get_year_range(self):
        """ return the range of years present in the database (useful for generating the summary statistics table) """
        YEAR_RANGE_CACHE_KEY = '%s.get_year_range' % self.__module__
        
        cached_year_range = cache.get(YEAR_RANGE_CACHE_KEY)
        if cached_year_range is not None:
            return cached_year_range        
        
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute('SELECT MIN(fiscal_year), MAX(fiscal_year) FROM %s LIMIT 1' % self.DJANGO_MODEL._meta.db_table)
        for row in cursor.fetchall():
            r = range(int(row[0]), int(row[1]))

        cache.set(YEAR_RANGE_CACHE_KEY,r)
        
        return r

    
    def _run_solr_query_if_necessary(self):
        # run raw solr query
        if self.SearchQuerySet is None:
            query = self._build_solr_query()            
            self.SearchQuerySet = SearchQuerySetWrapper().raw_search(query, rows=50)
    
    # # DEPRECATED -- returns bad data by allowing haystack to re-run the search
    # # TODO: determine if this is actually used; if not, remove it
    # def results(self):
    #     self._run_solr_query_if_necessary()
    #     return self.SearchQuerySet
                    
    def count(self):
        self._run_solr_query_if_necessary()
        return self.SearchQuerySet.__len__()

    def get_haystack_queryset(self, order_by='-obligation_date'):
        """ Returns a Haystack QuerySet object with the appropriate filters """        
        
        # order AND filters first, then OR filters
        and_filters = {}
        or_filters = {}
        for f in self.filters:
            filter_field = f[0]
            filter_value = f[1]
            filter_conjunction = f[2]

            # select appropriate target list
            target_filter_list = and_filters
            if f[2]==self.CONJUNCTION_OR:
                target_filter_list = or_filters
                        
            # deal with fk
            if self.FIELD_MAPPINGS[filter_field]['type']=='fk':
        
                field_operator = filter_field + '__in'
                fk_transformation = self.FIELD_MAPPINGS[filter_field].get('solr_transformation', lambda x: x)
        
                if type(filter_value) not in (list, tuple):
                    filter_value = (filter_value,)
        
                fk_values = []
                for value in filter_value:
                    fk_value = fk_transformation(value)
                    if fk_value is not None:
                        fk_values.append(str(fk_value))                                        

                target_filter_list[field_operator] = fk_values                
    
            # deal with range
            if self.FIELD_MAPPINGS[filter_field]['type']=='range':
                clause_parts = []
                range_transformation = self.FIELD_MAPPINGS[filter_field].get('solr_transformation', lambda x: x) # putting this in place
                filter_operators = ('__gte', '__lte')
                
                for i, range_specifier in enumerate(filter_value):
                    if range_specifier is not None:
                        target_filter_list[self.FIELD_MAPPINGS[filter_field]['solr_field'] + filter_operators[i]] = range_specifier                

            # deal with text
            elif self.FIELD_MAPPINGS[filter_field]['type']=='text':
                target_filter_list[filter_field] = filter_value
            
    
        s = SearchQuerySet().models(self.DJANGO_MODEL)
        
        # add sector filtering -- only works for a single sector at the moment
        if len(self.sectors):
            s = s.filter_and(sectors__in=map(lambda x: int(x.id), self.sectors))
        
        if len(or_filters):
            s = s.filter_or(**or_filters)

        if len(and_filters):
            s = s.filter_and(**and_filters)
        
        s = s.order_by(order_by)
        
        return s


class SearchQuerySetWrapper(SearchQuerySet):
    """ overrides the __len__() function to provide a correct hit count for raw searches """
    def __init__(self, *args, **kwargs):
        super(SearchQuerySetWrapper, self).__init__(*args, **kwargs)    

    def count(self):
        try:
            return int(self.query._hit_count)
        except Exception, e:
            return 0
            
            
# convenience methods and classes for search view

# DecimalField helpers from:
# http://www.djangosnippets.org/snippets/842/

class USDecimalHumanizedInput(forms.TextInput):
  def __init__(self, initial=None, *args, **kwargs):
    super(USDecimalHumanizedInput, self).__init__(*args, **kwargs)
  
  def render(self, name, value, attrs=None):
    if value != None:
        value = intcomma(value)
    else:
        value = ''
    return super(USDecimalHumanizedInput, self).render(name, value, attrs)



class USDecimalHumanizedField(forms.DecimalField):
  """
  Use this as a drop-in replacement for forms.DecimalField()
  """
  widget = USDecimalHumanizedInput
  
  def clean(self, value):
    value = value.replace(',','').replace('$','')
    super(USDecimalHumanizedField, self).clean(value)
    
    if value == '':
        value = None
    
    return value


