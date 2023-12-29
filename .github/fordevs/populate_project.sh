# Run the migrations
echo "Applying migrations..."
python manage.py migrate

# List of applications separated by spaces
apps="moneytracker"
echo $apps

# Run the sync_assets.py script
echo "Syncing assets..."
python -m core.sync_assets

# Iterate over each application and load its data
for app in $apps; do
    json_file="$app/data_init.json"
    if [ -f $json_file ]; then
        echo "Loading data for $app from $json_file..."
        python manage.py loaddata $json_file
    else
        echo "No data file found for $app"
    fi
done

# Create superuser
echo "Dont forget create the super user!"
python manage.py createsuperuser

echo "Data loading complete!"