'''
Created on 13. 9. 2012.

@author: Matija Piskorec
'''
from foc.visualiser.data_organiser.iorganiser import IOrganiser
from dracula.exceptions import NonExistentDataError
from foc.forecaster.ai.crisis_seer import CrisisSeer

from csv import reader
from pandas import MultiIndex, Series

class ScatterMatrixOrganiser(IOrganiser):
    '''
    Organises data for a scatter matrix visualization.
    (this is basically just convenient csv representation in json)
    '''

    def __init__(self):
        IOrganiser.__init__(self)
        

    def _organise_data(self, conf):
        
        arg = self._extractor.arg()
        arg["country_codes"] = conf.countries
        arg["indicator_codes"] = conf.indicators
        #arg["rca_indicator_codes"] = conf.rcaIndicators
        arg["interval"] = (conf.start_date, conf.end_date)
        countries = self._extractor.grab(arg)
        #TODO: add the process method somewhere inside the preprocessor
        #self._extractor.process(conf.process_indicators,
        #                           method = "slope",
        #                           look_back_years=conf.look_back_years)
        print("organiser got back:")
        print(countries)
        
        values = []
        
        for country in countries:
            years = range(conf.start_date, conf.end_date)
            crisis_seer = CrisisSeer(conf.sample_selection_file)
            crisis_years = crisis_seer.get_crisis_years(country.code)
                
            all_x = []
            for t in years:
                x = {}

                x['country'] = country.code
                x['date'] = t
                x['crisis'] = t in crisis_years
                emptyIndicators = 0
                for indicator_code in country.indicator_codes:
                    indicator = country.get_indicator(indicator_code)
                    try:
                        x[indicator_code] = indicator.get_value_at(t)      
                    except NonExistentDataError:
                        x[indicator_code] = ""
                        emptyIndicators = emptyIndicators + 1
                if (len(country.indicator_codes)==emptyIndicators): continue
                all_x.append(x)

            values = values + all_x
        
        self.vis_data = {'countries': conf.countries, 'indicators': conf.indicators, 'values': values}
        
        return self.vis_data

