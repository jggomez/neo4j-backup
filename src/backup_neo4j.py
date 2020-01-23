import os
import datetime
import zipfile
from google.cloud import storage

URL_BACKUP = '/home/juan/backups/'
BUCKET_NAME = "backups-wordbox"
NAME_DIRECTORY = "neo4j_backup"
NAME_FILE_ZIP = "neo4j_backup.zip"
URL_BACKUP_FILE_ZIP = URL_BACKUP + NAME_FILE_ZIP
FROM_SERVER = 'localhost:6362'
BACKUP_CMD = 'sudo neo4j-admin backup --backup-dir={} --from={} --name={}'
FORMAT_DATE = '%m-%d-%Y_%H-%M-%S'
MESSAGE_UPLOAD_FILE = 'File {} uploaded to {}.'
ENVIRONMENT_VARIABLE_GCP = "GOOGLE_APPLICATION_CREDENTIALS"
ENVIRONMENT_VARIABLE_VALUE_GCP = '/home/juan/Backend-Backups-Utility-Neo4j/src/resources/wordboxdev-credentials-storage.json'


def execute_command_backup():
    backup_cmd_tmp = BACKUP_CMD.format(
        URL_BACKUP, FROM_SERVER, NAME_DIRECTORY)
    # Execute backup command
    return os.popen(backup_cmd_tmp).read()


def upload_backup_file(path_file_upload):
    date = datetime.datetime.today().strftime(FORMAT_DATE)
    name_file_tpm = os.path.basename(path_file_upload)
    uri_upload = date + "/" + name_file_tpm

    # Storage Client GCP
    os.environ[ENVIRONMENT_VARIABLE_GCP] = ENVIRONMENT_VARIABLE_VALUE_GCP
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(uri_upload)
    blob.upload_from_filename(path_file_upload)
    print(
        MESSAGE_UPLOAD_FILE.format(
            name_file_tpm, uri_upload
        )
    )


def zip_directory(path):
    with zipfile.ZipFile(URL_BACKUP_FILE_ZIP, 'w', zipfile.ZIP_DEFLATED) as file_write:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_write.write(os.path.join(root, file))


def remove_zip_file():
    os.remove(URL_BACKUP_FILE_ZIP)


def create_backup():
    execute_command_backup()
    zip_directory(URL_BACKUP + NAME_DIRECTORY)
    upload_backup_file(URL_BACKUP_FILE_ZIP)
    remove_zip_file()


create_backup()
