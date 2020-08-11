# Neo4j Backup with Python

Neo4j utility python program for backing up neo4j databases during the online period. This program compresses the generated backup folder and uploads it to Google Cloud Storage.

# Steps for the automated backup
 - [ ] Install python3 and pip3 at the server. You can use the following guides.

        https://realpython.com/installing-python/
        https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/
         
 - [ ] Download the python program on your server and install dependencies with the following command 

	```
	sudo -H pip3 install pyyaml
	sudo -H pip3 install -U PyYAML
	sudo -H pip3 install google-cloud-storage
	sudo -H pip3 install -Iv cryptography==1.4.0
	```

 - [ ] Modify the yaml file. Contains important parameters for the correct job.
 
	```
	urlbackup: /home/juan/backups
	bucketname: backups --> [The bucket in GCP]
	pathcreadentialsgcp: /home/juan/backups/credentials.json
	```
        
 - [ ] Install cron package for linux with the following commands
        
        apt-get update && apt-get upgrade
        sudo apt-get install cron
        systemctl status cron
        
 - [ ] Edit the cron jobs file with the following command
         
         crontab -e
         
 - [ ] Schedule the script via cron, in this example full backup is done every day at 5 am

        0 */24 * * * /usr/bin/python3 /home/juan/backups_program/backup_neo4j.py /home/juan/backups_program/config.yaml >> /home/juan/backups_program/logbackups.log 2>&1
      
