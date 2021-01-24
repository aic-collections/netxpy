import re
import datetime

class SearchMethods():
    
    def __init__(self, netxconn):
        self.isoDateRegex = r'^([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})$'
        self.isoDateCompiled = re.compile(self.isoDateRegex)
        self.netxconn = netxconn
        return
    
    def get_assets_by_query(self, query, complete=False, start=0, count=101):
        qparams = query[0]
        for q in qparams:
            if q == "range" or q == "exact":
                if "field" in qparams[q]:
                    if qparams[q]["field"] == "modDate" or qparams[q]["field"] == "creationDate" or qparams[q]["field"] == "importDate":
                        if "value" in qparams[q] and self.isoDateCompiled.match(qparams[q]["value"]):
                            qparams[q]["value"] = self._isoToMilliseconds(qparams[q]["value"])
                        if "min" in qparams[q] and self.isoDateCompiled.match(qparams[q]["min"]):
                            qparams[q]["min"] = self._isoToMilliseconds(qparams[q]["min"])
                        if "max" in qparams[q] and self.isoDateCompiled.match(qparams[q]["max"]):
                            qparams[q]["max"] = self._isoToMilliseconds(qparams[q]["max"])

        context_data = [
                        "asset.id",
                        "asset.attributes",
                        "asset.base",
                        "asset.file",
                        "asset.folders",
                    ]
        if complete:
            context_data = context_data + ["asset.proxies", "asset.views", "asset.relatedAssets"]
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
                    "data": context_data
                }
            ]
        }
        results = self.netxconn.execute(context)
        for r in results["results"]:
            r["creationDate_iso"] = self._millisecondsToIso(r["creationDate"])
            r["importDate_iso"] = self._millisecondsToIso(r["importDate"])
            r["modDate_iso"] = self._millisecondsToIso(r["modDate"])
        return results

    def get_assets_from_solr(self, queryHuman="", queryRaw="", start=0, count=101):
        qplus = "&fq=assetId:*&fq=name:*&rows=" + str(count) + "&start=" + str(start)
        q = "q=" + queryHuman + qplus
        if queryRaw != "":
            q = queryRaw + qplus

        file_props = {
            'ast_checksum_p': "checksum",
        }
        asset_props = {
            'assetId': "id",
            'name': "name",
            'file': "fileName",
            'ast_creationDate_d': "creationDate_iso",
            'ast_modDate_d': "modDate_iso",
            'ast_importDate_d': "importDate_iso"
        }
        folders_props = {
            'ast_catParentPath_ps': "path",
            'category': "id",
            'categoryName': "name",
            # 'categoryPath': "path",
        }
            
        assets = []
        results = self.netxconn.solrrequest(q)
        for d in results["response"]["docs"]:
            asset = {}
            attributes = {}
            file = {}
            folders = {'children': None}
            for f in d:
                if (f.startswith('attr_')):
                    attrname = f.replace('attr_', '')
                    attrname = attrname.replace('_', " ")
                    attributes[attrname] = list(set(d[f]))
                
                elif (f.startswith('file') and f != "file"):
                    attrname = f.replace('file', '')
                    attrname = attrname.lower()
                    file[attrname] = d[f]
                
                elif f in asset_props:
                    if "Date" in f:
                        asset[asset_props[f]] = d[f].replace('Z', '')
                    else:
                        asset[asset_props[f]] = d[f]
                
                elif f in file_props:
                    file[file_props[f]] = d[f]
                
                elif f in folders_props:
                    folders[folders_props[f]] = d[f][0]
            
            #asset["solr_doc"] = d
            file["url"] = "/file/asset/" + str(d["assetId"]) + "/original/attachment"
            
            asset["creationDate"] = self._isoToMilliseconds(asset["creationDate_iso"])
            asset["modDate"] = self._isoToMilliseconds(asset["modDate_iso"])
            asset["importDate"] = self._isoToMilliseconds(asset["importDate_iso"])
            
            asset["file"] = file
            asset["folders"] = [folders]
            asset["attributes"] = attributes
                
            assets.append(asset)
        return assets
        
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


    def _isoToMilliseconds(self, isoDate):
        dt = datetime.datetime.strptime(isoDate, "%Y-%m-%dT%H:%M:%S")
        return int(dt.timestamp() * 1000)

    def _millisecondsToIso(self, milliseconds):
        seconds = int(milliseconds / 1000)
        dt = datetime.datetime.fromtimestamp(seconds)
        return dt.isoformat()

