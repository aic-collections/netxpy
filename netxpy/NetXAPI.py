import random
import requests
import json
import time

from .NetXConn import NetXConn

from .methods.AssetMethods import AssetMethods
from .methods.FolderMethods import FolderMethods
from .methods.SearchMethods import SearchMethods

class NetXAPI:
    
    def __init__(self, config):
        config["apibase"] = config["netx"] + "/external/api/json"
        if "appbase" not in config:
            # This is an override in case the address of NetX's internal
            # api changes and this library is not updated.
            config["appbase"] = config["netx"] + "/x7/v1.2/json"
        
        self.netxconn = NetXConn(config)
        self.am = AssetMethods(self.netxconn)
        self.fm = FolderMethods(self.netxconn)
        self.sm = SearchMethods(self.netxconn)
        return


    # Asset Methods
    def get_asset(self, asset_id):
        return self.am.get_asset(asset_id)
        
    def get_asset_attributes(self, asset_id):
        return self.am.get_asset_attributes(asset_id)
        

    # Folder Methods
    def create_folder_from_path(self, netx_folder_path):
        return self.fm.create_folder_from_path(netx_folder)
        
    def delete_folder_from_path(self, netx_folder_path):
        return self.fm.delete_folder_from_path(netx_folder)
        
    def get_folder_by_path(self, netx_folder):
        return self.fm.get_folder_by_path(netx_folder)
        
    
    # Search Methods
    def get_assets_by_query(self, query):
        return self.sm.get_assets_by_query(query)
        
    def raw_search(self, query_str):
        return self.sm.raw_search(query_str)

    def search(self, query_str):
        return self.sm.search(query_str)
        
    
