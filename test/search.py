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