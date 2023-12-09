#!/bin/sh   

# Ask the user if they are sure they want to delete all data from the database
echo -n 'Are you sure you want to delete all data from the database? (y/n): '
read REPLY
if echo $REPLY | grep -iq '^y'; then
    echo 'Flushing the database...'
    python manage.py flush
    echo 'Database flushed successfully!'
else
    echo 'Operation canceled.'
fi