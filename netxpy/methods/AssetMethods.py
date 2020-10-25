from .SearchMethods import SearchMethods

class AssetMethods():
    
    def __init__(self, netxconn):
        self.netxconn = netxconn
        self.sm = SearchMethods(netxconn)
        return
    
    def get_asset(self, asset_id):
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
        results = self.sm.get_assets_by_query(query)
        return results["results"][0]

    def get_asset_attributes(self, asset_id, True):
        context = {
            'method': 'getAssetAttributes',
            'params': [
                self.netxconn.session_key, 
                asset_id
            ]
        }
        return self.netxconn.execute(context)