import unittest
import os

import json

from netxpy.NetXAPI import NetXAPI

class SearchTestCase(unittest.TestCase):

    def setUp(self):
        path = os.path.abspath(__file__)
        dir = os.path.dirname(path) 
        with open(dir + '/config.json') as json_data:
            config = json.load(json_data)
        self.netxapi = NetXAPI(config)

    ### Objects ###
    def test_search(self):
        results = self.netxapi.search('assetId:362741')
        self.assertEqual(results["results"][0]["assetId"], 362741)
        
    def test_raw_search(self):
        results = self.netxapi.raw_search('assetId:362741')
        self.assertEqual(results["results"][0]["assetId"], 362741)
        
    def test_get_assets_by_query_date_range(self):
        query = [
            {
                "operator": "and",
                "range": {
                    "field": "importDate",
                    "min": "2020-07-20T22:23:20",
                    "max": "2020-07-20T22:23:40",
                    "includeMin": True,
                    "includeMax": True
                }
            }
        ]
        results = self.netxapi.get_assets_by_query(query)
        self.assertGreater(results["size"], 10)
        
    def test_solr_search(self):
        results = self.netxapi.get_assets_from_solr("assetId:188930")
        self.assertEqual(results["results"][0]["id"], 188930)

