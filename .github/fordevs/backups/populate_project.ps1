# Change to the directory where manage.py is located
Set-Location -Path .

# Execute the migrations
Write-Output 'Applying migrations...'
python manage.py migrate

# List of applications separated by commas
$apps = 'moneytracker'

# Iterate over each application and load its data
foreach ($app in $apps -split ',') {
    $json_file = Join-Path $app "data_init.json"
    if (Test-Path $json_file) {
        Write-Output "Loading data for $app from $json_file..."
        python manage.py loaddata $json_file
    } else {
        Write-Output "No data file found for $app"
    }
}

# Create superuser
Write-Output 'Don''t forget to create the superuser!'
python manage.py createsuperuser

Write-Output 'Data loading complete!'