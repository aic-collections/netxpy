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
        results = self.netxapi.get_asset_metadata(362741)
        self.assertEqual(results["id"], 362741)
        
    def test_get_asset_attributes(self):
        results = self.netxapi.get_asset_attributes(362741)
        # self.assertEqual(results["assetId_pub"][0], '362741')
        self.assertIn("LAKE UID", results)
    
    def test_fetch_asset_binary(self):
        response = self.netxapi.fetch_asset_binary(362741)
        # self.assertEqual(results["assetId_pub"][0], '362741')
        self.assertIn("Content-Disposition", response.headers)
        
    def test_download_asset_binary(self):
        response = self.netxapi.download_asset_binary(362741)
        # self.assertEqual(results["assetId_pub"][0], '362741')
        self.assertTrue(os.path.exists('/tmp/E33408.jpg'))
        if os.path.exists('/tmp/E33408.jpg'):
            os.remove('/tmp/E33408.jpg')