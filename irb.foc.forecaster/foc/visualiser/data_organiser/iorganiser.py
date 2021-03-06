'''
Created on 26. 6. 2012.

@author: kermit
'''

import json

from dracula.extractor import Extractor
from foc.forecaster.common.exceptions import MustOverrideError

class IOrganiser(object):
    '''
    Fetches data using the Extractor and organises it
    in json files for an appropriate visualisation presenter.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self._extractor = Extractor()
        # will store a dictionary with the necessary data
        self.vis_data = None
    
    def _write_data(self):
        """
        @param vis_data: a file where data
        should be stored   
        """
        filename = "data.json"
        with open(filename, "w") as out_file:
            json_text = json.dumps(self.vis_data, indent=4)
            out_file.write(json_text)
    
    def _organise_data(self, conf):
        """
        should use the extractor to fetch what is needed
        and format it in a dictionary (store in self.vis_data).
        @attention: must override
        """
        raise MustOverrideError
    
    def get_representation(self, conf):
        if conf.cache_enabled:
            self._extractor.enable_cache(conf.cache_host, conf.cache_port)
        self._organise_data(conf)
        if conf.cache_enabled and self._extractor.was_cached():
            print("Cache was hit, didn't have to query the World Bank API.")
        elif conf.cache_enabled:
            print("Data wasn't cached, queried the World Bank API.")
        #self._write_data()
        return self.vis_data
        
