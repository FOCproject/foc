'''
Created on 22. 8. 2012.

@author: kermit
'''

import copy

import wb.api
from cacher import Cacher


class Extractor(object):
    
    def __init__(self):
        self._cache_enabled = False
        self._cache_connection_port = None
        self._cache_connection_host = None
        self._cacher = None
        self._arg = {"country_codes" : ["hrv", "usa"],
               "indicator_codes" : ["SP.POP.TOTL"],
               "start_date":1980,
               "end_date":2010}

    def arg(self):
        return copy.deepcopy(self._arg)
    
    def normalize(self, arg):
        if arg==None:
            arg = self.arg()
        if "interval" in arg:
            arg["start_date"], arg["end_date"] = arg["interval"]
        capitalize_list = lambda elems : [el.upper() for el in elems]
        arg["country_codes"] = capitalize_list(arg["country_codes"])
        return arg
    
    def grab(self, arg=None, api=wb.api):
        #TODO: think about using kwargs
        """
        possible args are:
        
        1) the default by leaving None, defined in arg()
        2) setting your own such as:
                {"country_codes" : ["hrv", "usa", "chn"],
                   "indicator_codes" : ["SP.POP.TOTL"],
                   "start_date":1980,
                   "end_date":2010}
        3) using interval to set the dates more quickly (overrides start/end_date)
                {"country_codes" : ["hrv", "usa", "chn"],
                   "indicator_codes" : ["SP.POP.TOTL"],
                   "interval":(1980,2010)}
        """
        self.normalize(arg)
        if self._cache_enabled:
            countries = self._cacher.retreive(arg)
            if countries: cache_hit = True
            else: cache_hit = False
        if not self._cache_enabled or not cache_hit:
            countries = api.query_multiple_data(
                                                   arg["country_codes"], arg["indicator_codes"],
                                                   arg["start_date"], arg["end_date"])
            if self._cache_enabled and not cache_hit:
                self._cache(countries)
        return countries
    
    def enable_cache(self, host, port):
        self._cache_connection_host = host
        self._cache_connection_port = port
        self._cache_enabled = True
        self._cacher = Cacher(self._cache_connection_host, self._cache_connection_port)
        
    def disable_cache(self):
        self._cache_enabled = False
    
    def _cache(self,countries):
        if self._cache_enabled:
            self._cacher.cache(countries)
        else: return
    
    def is_cached(self, arg):
        self.normalize(arg)
        countries = self._cacher.retreive(arg)
        if countries: return True
        else: return False