# neo4j-backup-python

Neo4j utility python program for backing up neo4j databases during the online period. This program compresses the generated backup folder and uploads it to Google Cloud Storage.


# Cron Schedule

Schedule the script via cron (or any other scheduler you like), in this example full backup is done every day at 5 am

    0 5 * * * /usr/bin/python3 backup_neo4j.py > /backups/logbackup.log 2>&1


@jggomezt
