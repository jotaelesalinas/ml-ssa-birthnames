import os
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.sql import select, and_, or_, not_
import csv
import pprint

class CsvGenerator:
    
    def __init__(self):
        self._data = {}
        self._keys = set()
        
        self._db = create_engine('sqlite:///' + self._find_db_file())
        self._db.echo = False
        metadata = MetaData(self._db)
        self._top_100 = Table('top_100_per_year', metadata, autoload=True)
        self._scores = Table('scores', metadata, autoload=True)

        self._parse()
        self._write_output()
        
    def _find_db_file(self):
        dir = os.path.dirname(__file__) + '/'
        file = 'data/ssa_gov.sqlite'
        
        n = 1
        while not os.path.exists(dir + file):
            n += 1
            if n > 5:
                return None
            dir = dir + '../'
        
        return os.path.abspath(dir + file).replace('\\', '/')

    def _parse(self):
        s1 = select([self._top_100])
        result_top_100 = self._db.execute(s1)

        #n = 1
        for top in result_top_100:
            #n += 1
            #if n > 400: break
            
            print('_parse()', top)
            
            s2 = select([self._scores]).where(
                and_(
                    self._scores.c.year == top.year,
                    self._scores.c.name == top.name,
                    self._scores.c.gender == top.gender
                )
            )
            result_scores = self._db.execute(s2)
            
            m = 1
            for score in result_scores:
                m += 1
                #if m > 10: break
            
                self._add(top.year, top.name, top.gender, score.year, score.state, score.count, score.score, score.score2)
            
    def _add(self, year, name, gender, item_year, item_state, item_count, item_score, item_score2):
        for x in range(0,6):
            self._create(year + x, name, gender)
            self._assign(year + x, name, gender, item_year, item_state, item_count, item_score, item_score2)
        
    def _create(self, year, name, gender):
        if not gender in self._data:
            self._data[gender] = {}
        
        if not year in self._data[gender]:
            self._data[gender][year] = {}
        
        if not name in self._data[gender][year]:
            self._data[gender][year][name] = {}
    
    def _assign(self, year, name, gender, item_year, item_state, item_count, item_score, item_score2):
        key = item_state + '_n'
        if item_year < year:
            key += '_' + str(year - item_year)
        self._data[gender][year][name][key] = item_count
        self._keys.add(key)
         
        key = item_state + '_x'
        if item_year < year:
            key += '_' + str(year - item_year)
        self._data[gender][year][name][key] = item_score
        self._keys.add(key)
        
        key = item_state + '_xx'
        if item_year < year:
            key += '_' + str(year - item_year)
        self._data[gender][year][name][key] = item_score2
        self._keys.add(key)
        
    def _write_output(self):
        with open(os.path.dirname(__file__) + '/../data/female_5_years.csv', 'wt') as csv_f:
            csvwriter = csv.writer(csv_f, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            
            headers = list(self._keys)
            headers.sort()
            csvwriter.writerow(['Name_Year'] + headers)
            
            for year in self._data['f']:
                # xxx skip first and last n years (5)
                
                for name in self._data['f'][year]:
                    row = []
                    row.append(name + '_' + str(year))
                    
                    for h in headers:
                        if h in self._data['f'][year][name]:
                            row.append(self._data['f'][year][name][h])
                        else:
                            row.append(0)
            
                    csvwriter.writerow(row)
        
        with open(os.path.dirname(__file__) + '/../data/male_5_years.csv', 'wt') as csv_f:
            csvwriter = csv.writer(csv_f, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
            
            headers = list(self._keys)
            headers.sort()
            csvwriter.writerow(['Name_Year'] + headers)
            
            for year in self._data['m']:
                # xxx skip first and last n years (5)
                
                for name in self._data['m'][year]:
                    row = []
                    row.append(name + '_' + str(year))
                    
                    for h in headers:
                        if h in self._data['m'][year][name]:
                            row.append(self._data['m'][year][name][h])
                        else:
                            row.append(0)
            
                    csvwriter.writerow(row)
        
gen = CsvGenerator()
