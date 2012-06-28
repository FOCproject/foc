'''
Created on 14. 12. 2011.

@author: kermit
'''

class Country(object):
    '''
    __indicators concerning a single country
    '''
    #__code = ""
    #__indicators = {}

    def __init__(self, code):
        '''
        __code - code of a country
        '''
        self.__code = code
        self.code_iso2 = ""
        self.__indicators = {}
        self.__indicator_codes = []
    
    def __str__(self):
        return self.get_code()
    
    def __repr__(self):
        return self.get_code()

    def get_code(self):
        return self.__code

        
    def indicator_codes(self):
        return self.__indicator_codes
    
    def get_indicator(self, code):
        return self.__indicators[code]


    def set_indicator(self, indicator):
        self.__indicators[indicator.code] = indicator
        self.__indicator_codes.append(indicator.code)


    def del_indicators(self):
        del self.__indicators
        del self.__indicator_codes

    #__indicators = property(get_indicator, set_indicator, del_indicators,
    #                      "a dictionary with individual __indicators")
    code = property(get_code, None, None, None)
        
    