import unittest
import os

import json

from netxpy.NetXAPI import NetXAPI

class AssetTestCase(unittest.TestCase):

    def setUp(self):
        path = os.path.abspath(__file__)
        dir = os.path.dirname(path) 
        with open(dir + '/config.json') as json_data:
            config = json.load(json_data)
        self.netxapi = NetXAPI(config)

    ### Objects ###
    def test_get_asset(self):
        results = self.netxapi.get_asset(362741)
        self.assertEqual(results["assetId"], 362741)
        
    def test_get_asset_attributes(self):
        results = self.netxapi.get_asset_attributes(362741)
        # self.assertEqual(results["assetId_pub"][0], '362741')
        self.assertIn("LAKE UID", results)