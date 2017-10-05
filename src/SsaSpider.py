import os
import re
import logging
import scrapy
from scrapy import signals
from scrapy import Spider
from sqlalchemy import *
from sqlalchemy.orm import *

class CountryData(object):
    def __init__(self, year, pos, name, gender, count):
        self.year = year
        self.pos = pos
        self.name = name
        self.gender = gender
        self.count = count

class StateData(object):
    def __init__(self, year, state, pos, name, gender, count):
        self.year = year
        self.state = state
        self.pos = pos
        self.name = name
        self.gender = gender
        self.count = count

logging.getLogger('scrapy').setLevel(logging.WARNING)

class SsaSpider(Spider):
    name = "SsaSpider"
    
    # these values can be extracted from the website itself,
    # so they are always up to date
    _states = ('AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY')
    _year_init = 1960
    _year_end = 2016
    
    _url_year_country = 'https://www.ssa.gov/cgi-bin/popularnames.cgi'
    _url_year_state = 'https://www.ssa.gov/cgi-bin/namesbystate.cgi'
    
    _db_path = None
    
    _saver = None
    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(SsaSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider
    
    def start_requests(self):
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

    def parse_country(self, response):
        if self._saver == None: raise Exception('Saver not set in SsaSpider.')
        
        # xxx check that response code is 200
        data = self.extract_country_data(response)
        year = response.meta['year']
        
        print('Year:', year)
        
        for item in data:
            item['year'] = year
            obj = CountryData(**item)
            self._saver.send(obj)
    
    def parse_state(self, response):
        if self._saver == None: raise Exception('Saver not set in SsaSpider.')
        
        # xxx check that response code is 200
        data = self.extract_state_data(response)
        year = response.meta['year']
        state = response.meta['state']
        
        for item in data:
            item['year'] = year
            item['state'] = state
            obj = StateData(**item)
            self._saver.send(obj)
    
    def extract_country_data(self, response):
        data = []
        
        for table in response.css('table'):
            summary = table.xpath('@summary').extract()
            if len(summary) == 0: continue
            elif summary[0] != 'Popularity for top 1000': continue
            
            n = 0
            for tr in table.css('tr'):
                n = n + 1
                if n == 1: continue
                
                cells = tr.css('td ::text').extract()
                if not re.match(r'^\d+$', cells[0]): continue
                
                data.append({
                    "pos": cells[0],
                    "name": cells[1],
                    "gender": 'm',
                    "count": cells[2].replace(',', ''),
                })
                data.append({
                    "pos": cells[0],
                    "name": cells[3],
                    "gender": 'f',
                    "count": cells[4].replace(',', ''),
                })
            
            break
        
        return data
    
    def extract_state_data(self, response):
        data = []
        
        for caption in response.css('table > caption'):
            caption_text = caption.css('::text').extract_first()
            if not re.match(r'^Popularity for top 100 names in ', caption_text):
                continue
            
            table = caption.xpath('..')
            
            n = 0
            for tr in table.css('tr'):
                n = n + 1
                if n == 1: continue
                
                cells = tr.css('td ::text').extract()
                if not re.match(r'^\d+$', cells[0]): continue
                
                data.append({
                    "pos": cells[0],
                    "name": cells[1],
                    "gender": 'm',
                    "count": cells[2].replace(',', ''),
                })
                data.append({
                    "pos": cells[0],
                    "name": cells[3],
                    "gender": 'f',
                    "count": cells[4].replace(',', ''),
                })
            
            break
        
        return data
    
    def db_saver(self):
        # init db
        print('Opening DB...')
        self._db_path = self.find_db_file()
        if self._db_path == None: raise Exception('Database file not found in data/ssa_gov.sqlite.')
        
        db = create_engine('sqlite:///' + self._db_path)
        db.echo = False
        metadata = MetaData(db)
        states = Table('state_level', metadata, autoload=True)
        country = Table('country_level', metadata, autoload=True)
        
        # xxx empty both tables
        
        statesmapper = mapper(StateData, states)
        countrymapper = mapper(CountryData, country)
        
        # Set up the session
        sm = sessionmaker(bind=db, autoflush=False, autocommit=False,
            expire_on_commit=True)
        session = scoped_session(sm)
        
        print('Emptying tables...')
        session.execute('DELETE FROM state_level')
        session.execute('DELETE FROM country_level')
        session.flush()
        session.commit()
        
        n = 0
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
            
            session.add(entity)
            
            n += 1
            if n % 1000 == 0:
                session.flush()
            
            
        print('Flushing DB...')
        session.flush()
        session.commit()
        print('DB flushed and commited.')
    
    def find_db_file(self):
        dir = os.path.dirname(__file__) + '/'
        file = 'data/ssa_gov.sqlite'
        
        n = 1
        while not os.path.exists(dir + file):
            n += 1
            if n > 5:
                return None
            dir = dir + '../'
        
        return os.path.abspath(dir + file).replace('\\', '/')
    
    def spider_opened(self, spider):
        # second param is instance of spder about to be closed.
        print('Starting saver...')
        self._saver = self.db_saver()
        self._saver.send(None)
    
    def spider_closed(self, spider):
        # second param is instance of spder about to be closed.
        print('Finishing saver...')
        try:
            self._saver.send(None)
        except StopIteration:
            pass
