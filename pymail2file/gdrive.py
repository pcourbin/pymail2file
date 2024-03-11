from pydrive2.drive import GoogleDrive
from pydrive2.auth import GoogleAuth
import io

class GDrive:
    _main_folder = None
    _main_folder_id = None
    _gauth = None
    _drive = None

    def __init__(self, main_folder):
        self._main_folder = main_folder
        self._gauth = GoogleAuth()
        self._drive = GoogleDrive(self._gauth)
        self._main_folder_id = self.get_folder_id_from_path(main_folder, create=True)
        
    def get_file_list(self, parent_directory_id):
        foldered_list=self._drive.ListFile({'q':  "'"+parent_directory_id+"' in parents and trashed=false"}).GetList()
        return foldered_list

    def get_id_of_title(self, title, parent_directory_id):
        foldered_list=self._drive.ListFile({'q':  "'"+parent_directory_id+"' in parents and trashed=false"}).GetList()
        for file in foldered_list:
            if(file['title']==title):
                return file['id']
        return None

    def get_folder_id_from_path(self, path, create=True):
        folder_list = path.split("/")
        current_folder_id = 'root'
        for folder in folder_list:
            folder_id = self.get_id_of_title(folder, current_folder_id)
            if folder_id is None:
                if create:
                    newFolder = self._drive.CreateFile({'title': folder, "parents": [{"kind": "drive#fileLink", "id": \
                    current_folder_id}],"mimeType": "application/vnd.google-apps.folder"})
                    newFolder.Upload()
                    folder_id = newFolder['id']
                else:
                    return None
            current_folder_id = folder_id
        return current_folder_id

    def upload_file(self, folder_id, filename, payload, content_type):
        metadata = {
            'parents': [
                {"id": folder_id}
            ],
            'title': filename,
            'mimeType': content_type
        }
        file = self._drive.CreateFile(metadata=metadata)
        # Buffered I/O implementation using an in-memory bytes buffer.
        file.content = io.BytesIO(payload)
        file.Upload()
        return file['id']

    def upload_file_to_folder(self, folder_path, filename, payload, content_type):
        folder_id = self.get_folder_id_from_path(folder_path, create=True)
        return self.upload_file(folder_id, filename, payload, content_type)
