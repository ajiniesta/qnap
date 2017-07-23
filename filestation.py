import os

from qnap import Qnap

class FileStation(Qnap):
    """
    Access QNAP FileStation.
    """

    def list_share(self):
        """
        List all shared folders.
        """
        return self.req(self.endpoint(
            func='get_tree',
            params={
                'is_iso': 0,
                'node': 'share_root',
            }
        ))

    def list(self, path, limit=10000):
        """
        List files in a folder.
        """
        return self.req(self.endpoint(
            func='get_list',
            params={
                'is_iso': 0,
                'limit': limit,
                'path': path
            }
        ))

    def get_file_info(self, path):
        """
        Get file information.
        """
        dir_path = os.path.dirname(path)
        file_name = os.path.basename(path)
        return self.req(self.endpoint(
            func='stat',
            params={
                'path': dir_path,
                'file_name': file_name
            }
        ))

    def search(self, path, pattern):
        """
        Search for files/folders.
        """
        return self.req(self.endpoint(
            func='search',
            params={
                'limit': 10000,
                'start': 0,
                'source_path': path,
                'keyword': pattern
            }
        ))

    def delete(self, path):
        """
        Delete file(s)/folder(s)
        """
        dir_path = os.path.dirname(path)
        file_name = os.path.basename(path)
        return self.req(self.endpoint(
            func='delete',
            params={
                'path': dir_path,
                'file_total': 1,
                'file_name': file_name
            }
        ))

    def download(self, path):
        """
        Download file.
        """
        dir_path = os.path.dirname(path)
        file_name = os.path.basename(path)
        return self.req_binary(self.endpoint(
            func='download',
            params={
                'isfolder': 0,
                'source_total': 1,
                'source_path': dir_path,
                'source_file': file_name
            }
        ))

    def upload(self, path, data, overwrite=True):
        """
        Upload file.
        """
        dir_path = os.path.dirname(path)
        file_path = path.replace('/', '-')
        file_name = os.path.basename(path)
        return self.req_post(self.endpoint(
            func='upload',
            params={
                'type': 'standard',
                'overwrite': 1 if overwrite else 0,
                'dest_path': dir_path,
                'progress': file_path
            }),
            files={
                'file': (
                    file_name,
                    data,
                    'application/octet-stream'
                )
            }
        )

    def mkdir(self, target):
        """
        Create a directory
        """
        path_separator = "/"
        destFolder = target.split(path_separator)[-1]
        destPath = reduce(lambda x,y: x + path_separator + y, target.split(path_separator)[0:-1])
        self.req(self.endpoint(
            func='createdir',
            params={
                'dest_folder': destFolder,
                'dest_path': destPath
            }
        ))

    def mkdir_rec(self, target):
        """
        Creates a directory, and the intermediate ones
        """
        path_separator = "/"
        reduce(lambda x,y: self.m2(x + path_separator + y), target.split(path_separator))

    def m2(self, x):
        self.mkdir(x)
        return x

    def copy(self, source_file, source_total=1, dest_file, mode=1, dup="copy"):
        path_separator = "/"
        file_name = target.split(path_separator)[-1]
        file_folder_name = reduce(lambda x,y: x + path_separator + y, target.split(path_separator)[0:-1])
        self.req(self.endpoint(
            func='copy',
            params={
                'source_file':file_name,
                'source_total':source_total,
                'source_path':file_folder_name,
                'dest_path':dest_file,
                'mode':mode,
                'dup':dup
            }
        ))
