#!/bin/bash

# Base paths setup
BASE_PATH="/path/to/the/project/MyMoneyUP"
FORDEVS_PATH="$BASE_PATH/.github/fordevs"

# Load env variables
. "$BASE_PATH/.env"

# Script variables setup
BACKUP_FILENAME="$FORDEVS_PATH/backups/backup_$(date +%Y%m%d_%H%M%S).dump"

# Set password
export PGPASSWORD=$DBPASSWORD_PROD

# Perform backup
pg_dump -h $DBHOST_PROD -p $DBPORT_PROD -U $DBUSER_PROD -d $DBNAME_PROD -F c -b -v -f $BACKUP_FILENAME

# Check backup status
if [ $? -eq 0 ]; then
    echo "Backup was successful"
    python "$FORDEVS_PATH/send_mail.py" "$BACKUP_FILENAME" "$EMAIL_USER_PROD" "$EMAIL_PASSWORD_PROD" \
                "recipient@email.com" "Successful backup" "The backup was successful. Please find the attached file."

else
    echo "Error performing the backup"
    python "$FORDEVS_PATH/send_mail.py" "$FORDEVS_PATH/backups/BACKUP.md" "$EMAIL_USER_PROD" "$EMAIL_PASSWORD_PROD" "recipient@email.com" \
                "Backup error" "There was an error performing the backup. Please check the system."
fi