# netxpy

`netxpy` is a pythonic wrapper for the [NetX API](https://kb.netx.net/kb/developer-tools/json-rpc-api). 
It offers a few additional enhancements over the official API and, for better or 
for worse, some simplifications.  Enhancements include, but are 
not necessary limited to: raw search (and raw results, if desired) against NetX's 
internal API, the one that its HTML web service uses.  This has the benefit of 
permitting you to search an Assets system properties/attributes, for example.  It is
also possible to retrieve the formatted raw search results, which provide a more pythonic
means to access an Asset's attributes.  Simplifications pertain mostly to defaulting 
the "data options" to everything.

This is not a complete implementation of NetX's API.  Time/need permitting, 
this library will be expanded.

### Methods

The NetX API methods currently supported:
- Folders
    - getFoldersByParent = `get_folders_by_parent(parent_id)`
    - getFoldersByNameFilter = `get_folders_by_name_filter(name_filter)`
    - getFolderByPath = `get_folder_by_path(netx_folder_path)`
    - createFolderFromPath = `create_folder_from_path(netx_folder_path)`
- Assets
    - getAssetAttributes = `get_asset_attributes(asset_id)`
- Search
    - Note: `query` is a query object as defined by NetX.  See [https://kb.netx.net/kb/developer-tools/json-rpc-api#getAssetsByQuery](https://kb.netx.net/kb/developer-tools/json-rpc-api#getAssetsByQuery)
    - getAssetsByQuery = `get_assets_by_query(query[, start[, count]])`
    
Additional methods:
- Assets
    - `get_asset(asset_id)`
- Search
    - `raw_search(query_str[, start[, count]])`: This will return the 
            raw results from NetX's internal search API.  It is possible to search 
            system properties with this search.
    - `search(query_str[, start[, count]])`: This will return the 
            better formatted results from NetX's internal search API.  It is possible to search 
            system properties with this search.

### Basic Usage

```python
import json

from netxpy.NetXAPI import NetXAPI

config = {
        "netx": "https://netx.host",
        "user": "user",
        "pass": "pass"
    }

netxapi = NetXAPI(config)
r = netxapi.search("E33408")
print(r)
```

*More usage examples can be seen in the `test/` directory.*


### Installation

You'll probably just want to use pip to install netxpy:

    pip install git+https://github.com/aic-collections/netxpy.git

If you'd like to download and install the latest source you'll need git:

    git clone https://github.com/aic-collections/netxpy.git


### Developing

(Some) Unit tests are included.  You'll need [setuptools](https://pypi.python.org/pypi/setuptools#installation-instructions). 
Once you have the source and setuptools run the netxpy test:

    python setup.py test

