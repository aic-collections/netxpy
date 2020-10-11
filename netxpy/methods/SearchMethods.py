class SearchMethods():
    
    def __init__(self, netxconn):
        self.netxconn = netxconn
        return
    
    def get_assets_by_query(self, query):
        context = {
            'method': 'getAssetsByQuery',
            'params': [
                self.netxconn.session_key, 
                {"query": query},
                {
                    "data": [
                        "asset.id",
                        "asset.attributes",
                        "asset.base",
                        "asset.file",
                        "asset.proxies",
                        "asset.views",
                        "asset.relatedFolders",
                        "asset.folders",
                    ]
                }
            ]
        }
        return self.netxconn.execute(context)
        
    # This is basically a raw solr search
    def raw_search(self, query_str, start=1, count=101):
        ["sw6wqNxAlM2B87iepfR4EhXS6","fileName",0,0,[8],[4],[0],["modDate:[20200927170000 TO 20200927999999]"],[""],[""],1,41,[],"hybrid"]
        context = {
            'method': 'facetedSearch',
            'params': [
                self.netxconn.session_key, 
                "fileName", # Order by, more or less
                0,
                0,
                [8],
                [4],
                [0],
                [query_str],
                [""],
                [""],
                start, # Start
                count, # Count
                [],
                "hybrid" 
            ]
        }
        return self.netxconn.execute(context)
        
    def search(self, query_str, include_facets=False):
        results = self.raw_search(query_str)
        results.pop("assetIds", None)
        if not include_facets:
            results.pop("facets", None)
        for r in results["results"]:
            i = 0
            r["attributes"] = {}
            while i < len(r["attributeNames"]):
                a = r["attributeNames"][i]
                v = r["attributeValues"][i]
                r["attributes"][a] = []
                if (v != ""):
                    if (',' not in v):
                        r["attributes"][a].append(v)
                    else:
                        r["attributes"][a] = eval(v)
                i += 1
            keys = r.keys()
            for k in list(r):
                if (k.startswith('attribute') and k != "attributes"):
                    r.pop(k, None)
        return results
        
        
