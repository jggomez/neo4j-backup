import os
import datetime
import zipfile
import sys
import yaml
from google.cloud import storage


URL_BACKUP = 'urlbackup'  # '/home/juan/backups/'
BUCKET_NAME = 'bucketname'  # 'backups-wordbox'
# '/home/juan/Backend-Backups-Utility-Neo4j/src/resources/wordboxdev-credentials-storage.json'
URL_GCP_CREDENTIALS = 'pathcreadentialsgcp'
NAME_DIRECTORY = 'neo4j_backup'
NAME_FILE_ZIP = 'neo4j_backup.zip'
FROM_SERVER = 'localhost:6362'
BACKUP_CMD = 'sudo neo4j-admin backup --backup-dir={} --from={} --name={}'
FORMAT_DATE = '%m-%d-%Y_%H-%M-%S'
MESSAGE_UPLOAD_FILE = 'File {} uploaded to {}.'
ENVIRONMENT_VARIABLE_GCP = 'GOOGLE_APPLICATION_CREDENTIALS'


def validate_environment_variables(args):
    try:
        with open(args[1]) as file:
            config_list = yaml.load(file, Loader=yaml.FullLoader)

            global url_backup
            url_backup = config_list[URL_BACKUP]
        
            if(not url_backup):
                print('The config variable urlbackup doesnt exist')
                return False

            global bucket_name
            bucket_name = config_list[BUCKET_NAME]

            if(not bucket_name):
                print('The config variable bucketname doesnt exist')
                return False

            global path_credentials_gcp
            path_credentials_gcp = config_list[URL_GCP_CREDENTIALS]

            if(not path_credentials_gcp):
                print('The config variable pathcreadentialsgcp doesnt exist')
                return False
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise

    global url_backup_file_zip
    url_backup_file_zip = url_backup + NAME_FILE_ZIP

    return True


def execute_command_backup():
    backup_cmd_tmp = BACKUP_CMD.format(
        url_backup, FROM_SERVER, NAME_DIRECTORY)
    # Execute backup command
    return os.popen(backup_cmd_tmp).read()


def upload_backup_file(path_file_upload):
    date = datetime.datetime.today().strftime(FORMAT_DATE)
    name_file_tpm = os.path.basename(path_file_upload)
    uri_upload = date + "/" + name_file_tpm

    # Storage Client GCP
    os.environ[ENVIRONMENT_VARIABLE_GCP] = path_credentials_gcp
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(uri_upload)
    blob.upload_from_filename(path_file_upload)
    print(
        MESSAGE_UPLOAD_FILE.format(
            name_file_tpm, uri_upload
        )
    )


def zip_directory(path):
    with zipfile.ZipFile(url_backup_file_zip, 'w', zipfile.ZIP_DEFLATED) as file_write:
        for root, dirs, files in os.walk(path):
            for file in files:
                file_write.write(os.path.join(root, file))


def remove_zip_file():
    os.remove(url_backup_file_zip)


def create_backup():
    if(len(sys.argv) < 2):
        print('The arguments are invalid')
        return
    
    if(validate_environment_variables(sys.argv)):
        execute_command_backup()
        zip_directory(url_backup + NAME_DIRECTORY)
        upload_backup_file(url_backup_file_zip)
        remove_zip_file()


create_backup()
