"""
Script to sync assets from the Historic Crypto Library to the database.

This script uses the Historic Crypto Library to get the list of assets
from the Coinbase API and syncs them to the database.

Example:
    python -m core.sync_assets
"""
import json
import sys

import pandas as pd
import psycopg2
import requests
from psycopg2.extensions import connection

from .config_loader import load_config


def connect_db() -> connection:
    """
    Establish and return a connection to the database using env settings.

    Returns:
        psycopg2.extensions.connection: Database connection object.

    Raises:
        SystemExit: If connection to the database fails.
    """
    env_settings = load_config()
    # Connect to the database
    try:
        conn = psycopg2.connect(
            dbname=env_settings['DBNAME'],
            user=env_settings['DBUSER'],
            password=env_settings['DBPASSWORD'],
            host=env_settings['DBHOST'],
            port=env_settings['DBPORT']
        )
        print("Database connection successful.")
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        sys.exit(1)


def update_or_create_asset(conn: connection, name: str, price: str,
                           volume: str, symbol: str = '$',
                           asset_type: str = 'x') -> None:
    """
    Update an existing asset record or create a new one if it doesn't exist.

    Args:
        conn (psycopg2.extensions.connection): Database connection object.
        name (str): Name of the asset.
        price (str): Price of the asset.
        volume (str): Volume of the capitalization of the asset.
        symbol (str, optional): Symbol of the asset. Defaults to '$'.
        asset_type (str, optional): Type of the asset. Defaults to 'x'.
    """
    # Create a cursor
    with conn.cursor() as cursor:
        # Store the data in a variable
        data = (name, asset_type, price, volume, symbol[:9])

        # First, try to update the existing record
        cursor.execute(
            "UPDATE assets SET name = %s, type = %s, price = %s, volume = %s WHERE symbol = %s",  # noqa: E501
            data
        )
        # If no record was updated, then insert a new one
        if cursor.rowcount == 0:
            cursor.execute(
                "INSERT INTO assets (name, type, price, volume, symbol) VALUES (%s, %s, %s, %s, %s)",  # noqa: E501
                data
            )
        conn.commit()


def usd_assets():
    """Get USD assets from Coinbase API."""
    # Make a GET request to the Coinbase Products API
    response = requests.get("https://api.pro.coinbase.com/products")

    # If the status code of the response is in the successful range (200-204)
    if response.status_code in [200, 201, 202, 203, 204]:
        # Parse the response text to JSON and normalize the data
        response_data = pd.json_normalize(json.loads(response.text))

    # Query the DataFrame with the constructed query to retrieve data for
    # USD currency that's not delisted
    df_usd_currency = response_data.query(
        "quote_currency == 'USD' and status != 'delisted'"
    )
    return df_usd_currency


def get_crypto_ticker(id):
    """Get cryptocurrency ticker from Coinbase API."""
    # Send a GET request to Coinbase API to get the ticker for a specific
    # product
    response = requests.get(
        f'https://api.pro.coinbase.com/products/{id}/ticker'
    )
    # Check if status code indicates a successful response
    if response.status_code in [200, 201, 202, 203, 204]:
        ticker = json.loads(response.text)
        return ticker


if __name__ == '__main__':  # pragma: no cover
    # Get tickers from the Coinbase API
    coins = usd_assets()

    # Connect to the database
    conn = connect_db()

    # Iterate over the tickers and update/create in the database
    for index, row in coins.iterrows():
        display_name = row['display_name']
        symbol = row['id']
        # Get ticker of asset
        ticker = get_crypto_ticker(symbol)
        price = ticker['price']
        volume = ticker['volume']

        update_or_create_asset(conn, display_name, price, volume, symbol)
        print(f"Processing: {display_name} - {symbol}")

    conn.close()
    print("Database connection closed.")
