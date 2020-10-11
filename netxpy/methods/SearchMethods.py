class SearchMethods():
    
    def __init__(self, netxconn):
        self.netxconn = netxconn
        return
    
    def get_assets_by_query(self, query, start=0, count=101):
        context = {
            'method': 'getAssetsByQuery',
            'params': [
                self.netxconn.session_key, 
                {"query": query},
                {
                    "page": {
                        "startIndex": start,
                        "size": count
                    },
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
        
    # This searches Solr fields and attributes.
    def raw_search(self, query_str, start=1, count=101):
        ["sw6wqNxAlM2B87iepfR4EhXS6","fileName",0,0,[8],[4],[0],["modDate:[20200927170000 TO 20200927999999]"],[""],[""],1,41,[],"hybrid"]
        # AND search:
        ["7clgbZKDJdk66qg49SYVaPwnw","file",0,0,[8,8],[4,4],[0,0],["modDate:[20201004110000 TO 20201004110800]","Publish status:No"],["",""],["",""],1,41,[],"hybrid"]
        # OR search:
        ["7clgbZKDJdk66qg49SYVaPwnw","file",0,1,[8,8],[4,4],[0,0],["modDate:[20201004110000 TO 20201004110800]","Publish status:Web"],["",""],["",""],1,41,[],"hybrid"]
        
        query = []
        and_or = 0
        if (" AND " not in query_str and " OR " not in query_str):
            terms = [query_str]
        elif (" AND " in query_str):
            and_or = 1
            terms = query_str.split(" AND ")
        elif (" OR " in query_str):
            and_or = 1
            terms = query_str.split(" OR ")
        
        search_type = []
        something_else = []
        whatever_this_is = []
        and_whatever_this_is = []
        and_then_there_is_this_thing = []
        for t in terms:
            search_type.append(8)
            something_else.append(4)
            whatever_this_is.append("")
            and_whatever_this_is.append("")
            and_then_there_is_this_thing.append(0)
            query.append(t)
        
        context = {
            'method': 'facetedSearch',
            'params': [
                self.netxconn.session_key, 
                "file", # Order by, more or less
                0,
                and_or, # AND=0, OR=1
                search_type, # 8 is advanced
                something_else,
                and_then_there_is_this_thing,
                query,
                whatever_this_is,
                and_whatever_this_is,
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
        
        
