import os
import scrapy
from sqlalchemy import *

class SsaSpider(scrapy.Spider):
    name = "ssa"
    
    # these values can be extracted from the website itself,
    # so they are always up to date
    _states = ('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY')
    _year_init = 1960
    _year_end = 2016
    
    _url_year_country = 'https://www.ssa.gov/cgi-bin/popularnames.cgi'
    _url_year_state = 'https://www.ssa.gov/cgi-bin/namesbystate.cgi'
    
    # xxx
    _db_path = 'sqlite:///joindemo.db' 'sqlite:///%(here)s/data/ssa_gov.sqlite'
    
    class CountryData(object):
        pass
    
    class StateData(object):
        pass
    
    def start_requests(self):
        #self.log('================================================================')
        #self.log(__file__)
        #self.log(os.path.abspath(__file__))
        #self.log('================================================================')
        
        for year in range(self._year_init, self._year_end + 1):
            post_data = {"year": str(year), "top": '1000', "number": 'n'}
            req = scrapy.http.FormRequest(self._url_year_country, formdata=post_data, callback=self.parse_country)
            req.meta['year'] = year
            yield req
            
            for state in self._states:
                post_data = {"year": str(year), "state": state}
                req = scrapy.http.FormRequest(self._url_year_state, formdata=post_data, callback=self.parse_state)
                req.meta['year'] = year
                req.meta['state'] = state
                yield req
                break
            break

    def parse_country(self, response):
        # xxx check that response code is 200
        data = self.extract_country_data(response.body)
        year = response.meta['year']
    
    def parse_state(self, response):
        # xxx check that response code is 200
        data = self.extract_state_data(response.body)
        year = response.meta['year']
        state = response.meta['state']
    
    def extract_country_data(self, html):
        self.log('extract_country_data()')
        self.log(len(html))
    
    def extract_state_data(self, html):
        self.log('extract_state_data()')
        self.log(len(html))
    
    def db_saver(self):
        """Generator"""
        # init db
        db = create_engine(self._db_path)
        db.echo = True
        metadata = BoundMetaData(db)
        states = Table('state_level', metadata, autoload=True)
        country = Table('country_level', metadata, autoload=True)
        
        statesmapper = mapper(StateData, states)
        countrymapper = mapper(CountryData, country)
        
        session = create_session()
        
        while True:
            # read from yield
            entity = yield
            if entity == None: break
            
            if isinstance(entity, StateData):
                pass
            elif isinstance(entity, CountryData):
                pass
            else:
                raise "Wrong entity type"
            
            session.save(entity)
            
        # close db
        session.flush()
