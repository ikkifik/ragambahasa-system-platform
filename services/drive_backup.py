from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
import mysql.connector
import sys
import os

try:
    sys.path.append(".")
    from config import config
except:
    sys.path.append("..")
    from config import config

def init_db():
    db = mysql.connector.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PWD,
        database=config.DB_NAME
    )
    return db


def get_data_to_upload():
    query = 'SELECT pcid, file_path, is_moved FROM printed_content WHERE is_moved=0'
    db = init_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(query)
    result = cursor.fetchall()
    
    return result


def update_moved_path(moved_path, pcid):
    datenow = datetime.strftime(datetime.utcnow(), "%Y-%m-%d %H:%M:%S")
    query = 'UPDATE printed_content SET moved_path=%s, is_moved=1, moved_date=%s WHERE pcid=%s'
    db = init_db()
    cursor = db.cursor()
    cursor.execute(query, (moved_path, datenow, pcid))
    db.commit()
    
    now = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    print(f"{now} | {cursor.rowcount} record moved into cloud.")
    

def datenow():
    now = datetime.now()
    now = datetime.strftime(now, "%Y%m%d_%H%M%S")
    return now

def retrieve_file(filename, uploaded_file):
    import requests

    img_file_format = ['jpg', 'jpeg', 'png']
    doc_file_format = ['pdf', 'doc', 'docx', 'txt', 'odt']

    file_format = uploaded_file.split(".")[-1]
    retrieve_content = os.path.join(config.HOST_URL, uploaded_file)
    
    if not os.path.exists("temp"):
            os.mkdir("temp")
    filepath = os.path.join("temp", filename)
    
    if file_format.lower() in img_file_format:
        from PIL import Image
        img = Image.open(requests.get(retrieve_content, stream = True).raw)
        img.save(filepath)

    elif file_format.lower() in doc_file_format:
        with open(filepath, 'wb') as f:
            f.write(requests.get(retrieve_content, stream = True).content)
    
    return filepath

class DriveBackup:
    def __init__(self):
        self.gauth = GoogleAuth()

        # Try to load saved client credentials
        self.gauth.LoadCredentialsFile("service_credentials.txt")
        if self.gauth.credentials is None:
            # Authenticate if they're not there
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            # Refresh them if expired
            self.gauth.Refresh()
        else:
            # Initialize the saved creds
            self.gauth.Authorize()
        # Save the current credentials to a file
        self.gauth.SaveCredentialsFile("service_credentials.txt")
        
        self.drive = GoogleDrive(self.gauth)
        self.root_folder_id = config.DRIVE_FOLDER_ID

    def create_folder(self):
        # Folder create
        folder_name = datenow()+'_backup'
        folder_metadata = {
            'title' : folder_name, 
            'parents': [{'id': self.root_folder_id}], 
            'mimeType' : 'application/vnd.google-apps.folder'}

        folder = self.drive.CreateFile(folder_metadata)
        folder.Upload()
        
        return folder['id'], folder_name

    def upload_file(self, folder_id, folder_name, uploaded_file):
        file = self.drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folder_id}]})
        file['title'] = uploaded_file.split("/")[-2]+"_"+uploaded_file.split("/")[-1]

        tmp_path = ""
        try:
            file.SetContentFile(uploaded_file) # name the file 
        except:
            filepath = retrieve_file(filename=file['title'], uploaded_file=uploaded_file)
            file.SetContentFile(filepath)
            tmp_path = filepath

        file.Upload()
        
        moved_path = os.path.join("/", folder_name, file['title'])
        return moved_path, tmp_path

if __name__ == "__main__":
    
    drivebackup = DriveBackup()
    folder_id, folder_name = drivebackup.create_folder()
    
    data_list = get_data_to_upload()
    for dl in data_list:
        moved_path, tmp_path = drivebackup.upload_file(folder_id=folder_id, folder_name=folder_name, uploaded_file=dl['file_path'])
        update_moved_path(moved_path=moved_path, pcid=dl['pcid'])
        if tmp_path != "":
            os.remove(tmp_path)