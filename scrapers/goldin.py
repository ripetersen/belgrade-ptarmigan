import csv
import os
import sys
from bbc import user_agent

import argparse
import logging
import json
import re
import time
import random
import pandas as pd
import math
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import namedtuple

Query = namedtuple("Query", "type show_only")

FEATURED_QUERY = Query("Featured", None)
FACET_QUERY = Query("Facet", "Sold")
ENDING_SOONEST_QUERY = Query("Ending_Soonest", "Sold")

QUERY_MAP = {
    'all': {FEATURED_QUERY, FACET_QUERY, ENDING_SOONEST_QUERY},
    'featured': {FEATURED_QUERY},
    'facet': {FACET_QUERY},
    'ending-soonest': {ENDING_SOONEST_QUERY},
        }

class Scraper():
    def __init__(self, 
            start="https://goldin.co/buy/", 
            data_dir=None, 
            item_type=["Single Cards"], 
            sub_category=["Baseball"],
            query=QUERY_MAP['featured']):
        self._start = start
        self._data_dir = data_dir
        self._overwrites = False
        self._query = query
        self._search = {
            "queryType": "Featured",
            "item_type": item_type,
            "sub_category": sub_category,
            "size": 24,
            "from": 0,
            "auction_id": []
        }

        self._ua = user_agent.UserAgent(headers={
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9,da-DK;q=0.8,da;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'https://goldin.co',
        'Referer': 'https://goldin.co/',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',        
    })

    def get_client_js_url(self, url:str) -> str:
        r = self._ua.get(url)
        soup = BeautifulSoup(r.text,'html.parser')
        src = soup.find('script',{'src':re.compile('.+client\..+\.js')})['src']
        return urljoin(url, src)

    def get_client_js(self, url:str) -> str:
        response = self._ua.get(url)
        return response.text

    def extract_api_urls(self, client_js:str) -> dict:
        m = re.search('api:(.*)}},zkoo',client_js)
        api_json = m.group(1)
        json_str=re.sub('([{,])([a-zA-Z0-9_]+):','\\1"\\2":',api_json)
        return json.loads(json_str)

    def extract_cloudfront_url(self, client_js:str) -> str:
        m = re.search(',cloudFrontURL:"(.*?)"',client_js)
        return m.group(1)

    def get_auctions(self,status="Active") -> dict:
        auctions_url = self._api_urls['auctions']['url']
        r = self._ua.post(auctions_url, data={"status":status,"order":"asc"})
        return r.json()
    
    def extract_auction_ids(self, auction_response) -> list:
        return [auction['auction_id'] for auction in auction_response['auctions']]
    
    def get_lots(self) -> dict:
        lots_url = self._api_urls['lots_v2']['url']
        r = self._ua.post(lots_url, data={"search":self._search})
        return r.json()
    
    def save_lot(self, lot) -> str:
        if self._data_dir is None:
            return 
        lot_dir = os.path.join(self._data_dir, '_'.join(self._search["sub_category"]), lot['lot_id'])
        if os.path.exists(lot_dir):
            if not self._overwrites:
                logging.debug(f"Skipping {lot_dir}, exists")
                return
        else:
            os.makedirs(lot_dir)
        with open(os.path.join(lot_dir, 'lot.json'), 'w') as f:
            json.dump(lot, f, indent=4)
        primary_image_name = lot['primary_image_name']
        if primary_image_name.startswith('http') or primary_image_name.startswith('https'):
            image_url = primary_image_name
            if '/small/' in image_url:
                image_url = image_url.replace('/small/', '/large/')
            image_filename = os.path.basename(image_url)
        else:
            image_url = f"{self._image_url}/public/Lots/{lot['lot_id']}/{lot['primary_image_name']}@3x"
            image_filename = f"{lot['primary_image_name']}.jpg"
        r = self._ua.get(image_url)
        with open(os.path.join(lot_dir, image_filename), 'wb') as f:
            f.write(r.content)

        
    def scrape(self):
        # Get the client.js url
        client_js_url = self.get_client_js_url(self._start)
        # Get the client_js
        client_js = self.get_client_js(client_js_url)
        # Get the api urls
        self._api_urls = self.extract_api_urls(client_js)
        logging.debug(json.dumps(self._api_urls, indent=4))
        # Get the cloudfront url
        self._image_url=self.extract_cloudfront_url(client_js)
        logging.debug(f"cloudfront url {self._image_url}")
        # Get the auctions
        auctions_response = self.get_auctions()
        auctions_id = self.extract_auction_ids(auctions_response)
        auctions_response = self.get_auctions(status="All")
        auctions_id += self.extract_auction_ids(auctions_response)
        logging.debug(f"auctions_id {auctions_id}")
        self._search['auction_id'] = auctions_id
        # Get the lots
        for query in self._query:
            self._search['queryType'] = query.type
            if query.show_only is not None:
                self._search['show_only'] = query.show_only
            self._search['from'] += 0
            while True:
                lots_response = self.get_lots()
                #logging.debug(json.dumps(lots_response, indent=4))
                lots = lots_response['searchalgolia']['lots']
                logging.debug(f"Found {len(lots)} lots")
                if len(lots) == 0:
                    logging.debug("No more lots found")
                    break
                for lot in lots:
                    self.save_lot(lot)
                self._search['from'] += self._search['size']
                time.sleep(random.random()+0.5)
        #lots_response = self.get_lots(auctions_id)
        #logging.debug(json.dumps(lots_response, indent=4))

# Add CSG 
RATERS=['BGS','PSA','SGC','BVG','CSG','CGC']
RATERS_REGEX = "|".join([f"({r})" for r in RATERS])
GRADE_REGEX = re.compile(f'({RATERS_REGEX})(\\D+)([\\d.]+)')
def grade(scraper_args=[]):
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--data', default='data', help='data directory')
    argparser.add_argument('--sub-category', default=['Baseball'], nargs="*",  help='subcategory')
    args = argparser.parse_args(scraper_args)
    graded_count = 0
    error_count = 0
    not_found_count = 0

    lot_dir = os.path.join(args.data, '_'.join(args.sub_category))       
    for lot in os.listdir(lot_dir):
        lot_path = os.path.join(lot_dir, lot)
        if os.path.isdir(lot_path):
            lot_json = os.path.join(lot_path, 'lot.json')
            if os.path.exists(lot_json):
                with open(lot_json, 'r') as f:
                    try: 
                        lot_data = json.load(f)
                        match = re.search(GRADE_REGEX, lot_data['title'])
                        if not match:
                            print(f"\nCould not find grade in '{lot_data['title']}' @ {lot_json}")
                            not_found_count += 1
                        else:
                            graded_count += 1
                            sys.stdout.write('.')
                            grade_json = os.path.join(lot_path, 'grade.json')
                            with open(grade_json, 'w') as grade_file:
                                grading_agency = match.group(1).strip()
                                grade_note = match.group(len(RATERS)+2).strip()
                                grade = match.group(len(RATERS)+3).strip()
                                grade = float(grade) if '.' in grade else int(grade)
                                grade_file.write(json.dumps({"grading_agency":grading_agency,"grade":grade,"grade_note":grade_note}, indent=4))
                    except Exception as e:
                        print(f"\nError processing {lot_json} {e}")
                        error_count += 1
    print(f"\nGraded {graded_count} lots, {not_found_count} not found, {error_count} errors")

def tocsv(scraper_args=[]):
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--data', default='data', help='data directory')
    argparser.add_argument('--sub-category', default=['Baseball'], nargs="*",  help='subcategory')
    args = argparser.parse_args(scraper_args)
    lot_dir = os.path.join(args.data, '_'.join(args.sub_category))
    csv_filename = os.path.join(lot_dir, 'lots.csv')
    with open(csv_filename, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=['lot_id','title','status','min_bid_price', 'number_of_bids', 'current_price', 'agency', 'grade', 'grade_note'])
        writer.writeheader()
        for lot in os.listdir(lot_dir):
            lot_path = os.path.join(lot_dir, lot)
            lot_json = os.path.join(lot_path, 'lot.json')
            grade_json = os.path.join(lot_path, 'grade.json')
            if os.path.isdir(lot_path) and os.path.exists(lot_json) and os.path.exists(grade_json):
                with open(lot_json, 'r') as f:
                    lot_data = json.load(f)
                    with open(grade_json, 'r') as g:
                        sys.stdout.write('.')
                        grade_data = json.load(g)
                        writer.writerow({
                            'lot_id': lot_data['lot_id'],
                            'title': lot_data['title'].strip(),
                            'status': lot_data['status'],
                            'min_bid_price': lot_data['min_bid_price'],
                            'number_of_bids': lot_data['number_of_bids'],
                            'current_price': lot_data['current_price'],
                            'agency': grade_data['grading_agency'],
                            'grade': grade_data['grade'],
                            'grade_note': grade_data['grade_note'],
                            })
    ddescribe(scrape_args=scraper_args)

def describe(scraper_args=[]):
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--data', default='data', help='data directory')
    argparser.add_argument('--sub-category', default=['Baseball'], nargs="*",  help='subcategory')
    args = argparser.parse_args(scraper_args)
    lot_dir = os.path.join(args.data, '_'.join(args.sub_category))
    csv_filename = os.path.join(lot_dir, 'lots.csv')
    
    lots = pd.read_csv(csv_filename)
    print(lots)
    print(lots.describe())
    bins = [len(lots[(lots['grade']>=n) & (lots['grade']<n+1)]) for n in range(1,10)]
    pad = math.ceil(math.log10(max(bins)+1e-10))
    h = '\n'.join([f"{grade} ({str(n).rjust(pad)}) : {'='*int(40*n/max(bins))}" for grade,n in enumerate(bins,start=1)])
    print(h)


                    
def dedupe(scraper_args=[]):
    pass

def scrape(scraper_args=[]):
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--start', default='https://goldin.co/buy/', help='starting url')
    argparser.add_argument('--data', default='data', help='data directory')
    argparser.add_argument('--query', default=['featured'], nargs="*", help='query type')
    argparser.add_argument('--sub-category', default=['Baseball'], nargs="*",  help='subcategory')
    argparser.add_argument('--item-type', default=['Single Cards'], nargs="*",  help='item type')
    argparser.add_argument('--sold-only', action="store_true",  help='show sold')


    args = argparser.parse_args(scraper_args)
    if not os.path.exists(args.data):
        os.makedirs(args.data)

    query = set()
    for q in args.query:
        if q not in QUERY_MAP:
            print(f"Invalid query {q}")
            return
        query.update(QUERY_MAP[q])

    scraper = Scraper(args.start,data_dir=args.data,sub_category=args.sub_category,item_type=args.item_type,query=query)
    scraper.scrape()

EXPORT=['scrape','grade','tocsv','dedupe','describe']
