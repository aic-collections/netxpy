from .SearchMethods import SearchMethods

class AssetMethods():
    
    def __init__(self, netxconn):
        self.netxconn = netxconn
        self.sm = SearchMethods(netxconn)
        return
    
    def get_asset(self, asset_id):
        results = self.sm.search('assetId:' + str(asset_id))
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