# Neo4j Backup with Python

Neo4j utility python program for backing up neo4j databases during the online period. This program compresses the generated backup folder and uploads it to Google Cloud Storage.

# Steps for the automated backup
 - [ ] Install python3 and pip3 at the server. You can use the following guides.

        https://realpython.com/installing-python/
        https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/

- [ ] Create the environment variables permanently, and system wide (all users, all processes) add set variable in /etc/environment
 
        sudo vi /etc/profile.d/backup_neo4j.sh

 - [ ] Add a named environment variable to the /etc/environment file, with name URL_BACKUP then its value is the path of the disk where you want to save the backup.
 
        export URL_BACKUP=/home/juan/backups/
            
 - [ ] Add a named environment variable to the /etc/environment file, with name BUCKET_NAME then its value is the name of storage in GCP.
 
        export BUCKET_NAME=backups-wordbox
         
 - [ ] Add a named environment variable to the /etc/environment file, with name ENVIRONMENT_VARIABLE_VALUE_GCP then its value is the path of GCP credentials.
 
        export URL_GCP_CREDENTIALS=/home/juan/Backend-Backups-Utility-Neo4j/src/resources/wordboxdev-credentials-storage.json
         
 - [ ] Download the python program on your server and install dependencies with the following command 
 
		pip3 install google-cloud-storage
		pip3 install google-cloud
        
        
 - [ ] Install cron package for linux with the following commands
        
        apt-get update && apt-get upgrade
        sudo apt-get install cron
        systemctl status cron
        
 - [ ] Edit the cron jobs file with the following command
         
         crontab -e
         
 - [ ] Schedule the script via cron, in this example full backup is done every day at 5 am

        0 5 * * * /usr/bin/python3 /home/juan/backups_program/backup_neo4j.py > /backups/logbackup.log 2>&1
      
