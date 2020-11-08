import platform
import tempfile

from .SearchMethods import SearchMethods

class AssetMethods():
    
    def __init__(self, netxconn):
        self.netxconn = netxconn
        self.sm = SearchMethods(netxconn)
        return
    
    def download_asset_binary(self, asset_id, savedir="", filename="", binary_type="original"):
        if savedir == "":
            if 'tmpdir' in self.netxconn.config:
                savedir = self.netxconn.config["tmpdir"]
            else:
                tempdir = "/tmp" if platform.system() == "Darwin" else tempfile.gettempdir()
                savedir = tempdir + '/'
        return self.netxconn.download("/file/asset/" + str(asset_id) + "/" + binary_type + "/attachment", savedir, filename)
        
    def fetch_asset_binary(self, asset_id, binary_type="original"):
        return self.netxconn.fetch("/file/asset/" + str(asset_id) + "/" + binary_type + "/attachment")
    
    def get_asset_metadata(self, asset_id):
        # This performs a raw search against the facetsearch
        # results = self.sm.search('assetId:' + str(asset_id))
        query = [
            {
                "operator": "and",
                "exact": {
                    "field": "assetId",
                    "value": str(asset_id)
                }
            }
        ]
        results = self.sm.get_assets_by_query(query, True)
        return results["results"][0]

    def get_asset_attributes(self, asset_id):
        context = {
            'method': 'getAssetAttributes',
            'params': [
                self.netxconn.session_key, 
                asset_id
            ]
        }
        return self.netxconn.execute(context)