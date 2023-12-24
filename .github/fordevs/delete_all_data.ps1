# Ask the user if they are sure they want to delete all data from the database
$reply = Read-Host 'Are you sure you want to delete all data from the database? (y/n)'

# Check if the user's input starts with 'y' or 'Y'
if ($reply -match '^y') {
    Write-Host 'Flushing the database...'
    # Run the Python script using the Python interpreter
    python manage.py flush
    Write-Host 'Database flushed successfully!'
} else {
    Write-Host 'Operation canceled.'
}
