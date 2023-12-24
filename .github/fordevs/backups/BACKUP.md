# BackUp for DB PostgreSQL

In this directory you can find the backups of the database.
Obviously, the backup is not updated in real time, but it is updated every time a new version of the project is released.
And this dont have follow for git.

# Install

Install the PostgreSQL 16
```bash
sudo apt-get install postgresql-client-16
```
Copy the example script
```bash
cp .github/fordevs/backups/backup_db.example .github/fordevs/backups/backup_db.sh
```
Then change the BASE_PATH and the recipient email on the backup_db.sh script
+ Don't forget to update your environment variables!

Give permission to execute the script
```bash
chmod +x /path/to/project/MyMoneyUP/.github/fordevs/backups/backup_db.sh
```
Run it
```bash
sh .github/fordevs/backups/backup_db.sh
```
Or add the script to the crontab
```bash
crontab -e
```
Add the line below to the end of the file
```bash
59 17 * * * /path/to/project/MyMoneyUP/.github/fordevs/backups/backup_db.sh
```
# Backup Script Explanation

The actual backup of the PostgreSQL database is performed using the `pg_dump` command in the `backup_db.sh` script. Here's a breakdown of the command:

- `pg_dump`: This is the command used to backup a PostgreSQL database.
- `-h $DBHOST_PROD`: This specifies the host of the database.
- `-p $DBPORT_PROD`: This specifies the port of the database.
- `-U $DBUSER_PROD`: This specifies the user of the database.
- `-d $DBNAME_PROD`: This specifies the name of the database.
- `-F c`: This specifies the format of the backup file. The 'c' stands for custom format.
- `-b`: This includes large objects in the backup.
- `-v`: This enables verbose mode, which provides detailed object-by-object method.
- `-f $BACKUP_FILENAME`: This specifies the filename of the backup.