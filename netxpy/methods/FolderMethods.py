class FolderMethods():
    
    def __init__(self, netxconn):
        self.netxconn = netxconn
        return
    
    def create_folder_from_path(self, netx_folder_path):
        context = {
            'method': 'createFolderFromPath',
            'params': [
                self.netxconn.session_key, 
                netx_folder_path,
                {
                    "data": [
                        "folder.id",
                        "folder.base",
                        "folder.children"
                    ]
                }
            ]
        }
        return self.netxconn.execute(context)
    
    # Does this work?  It's not documented.
    def delete_folder_from_path(self, netx_folder_path):
        context = {
            'method': 'deleteFolderFromPath',
            'params': [
                self.netxconn.session_key, 
                netx_folder_path,
                {
                    "data": [
                        "folder.id",
                        "folder.base",
                        "folder.children"
                    ]
                }
            ]
        }
        return self.netxconn.execute(context)
        
    def get_folders_by_name_filter(self, name_filter):
        context = {
            'method': 'getFoldersByNameFilter',
            'params': [
                self.netxconn.session_key, 
                name_filter,
                {
                    "page": {
                    "startIndex": 0,
                    "size": 500
                },
                    "data": [
                        "folder.id",
                        "folder.base",
                        "folder.children"
                    ]
                }
            ]
        }
        return self.netxconn.execute(context)

    def get_folders_by_parent(self, parent_id):
        context = {
            'method': 'getFoldersByParent',
            'params': [
                self.netxconn.session_key, 
                parent_id,
                {
                    "page": {
                    "startIndex": 0,
                    "size": 500
                },
                    "data": [
                        "folder.id",
                        "folder.base",
                        "folder.children"
                    ]
                }
            ]
        }
        return self.netxconn.execute(context)

    def get_folder_by_path(self, netx_folder):
        context = {
            'method': 'getFolderByPath',
            'params': [
                self.netxconn.session_key, 
                netx_folder,
                {
                    "data": [
                        "folder.id",
                        "folder.base",
                        "folder.children"
                    ]
                }
            ]
        }
        return self.netxconn.execute(context)
