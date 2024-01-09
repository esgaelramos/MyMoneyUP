"""
Script to sync assets from the Historic Crypto Library to the database.

This script uses the Historic Crypto Library to get the list of assets
from the Coinbase API and syncs them to the database.

Example:
    python -m core.sync_assets
"""
import sys

import psycopg2
from psycopg2.extensions import connection
# from Historic_Crypto import Cryptocurrencies
from core.config_loader import load_config


top_30_crypto_pairs = [
    "BTC-USD", "ETH-USD", "SOL-USD", "ADA-USD", "XRP-USD", "DOT-USD",
    "DOGE-USD", "AVAX-USD", "LINK-USD", "LTC-USD", "BCH-USD", "ALGO-USD",
    "XLM-USD", "UNI-USD", "WBTC-USD", "ATOM-USD", "VET-USD", "FIL-USD",
    "SAND-USD", "RPL-USD", "XTZ-USD", "EOS-USD", "MKR-USD", "CRO-USD",
    "DASH-USD", "ZEC-USD"
]


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


def update_or_create_asset(conn: connection, name: str,
                           symbol: str = '$', asset_type: str = 'x') -> None:
    """
    Update an existing asset record or create a new one if it doesn't exist.

    Args:
        conn (psycopg2.extensions.connection): Database connection object.
        name (str): Name of the asset.
        symbol (str, optional): Symbol of the asset. Defaults to '$'.
        asset_type (str, optional): Type of the asset. Defaults to 'x'.
    """
    # Create a cursor
    with conn.cursor() as cursor:
        # Store the data in a variable
        data = (name, asset_type, symbol[:9])

        # First, try to update the existing record
        cursor.execute(
            "UPDATE assets SET name = %s, type = %s WHERE symbol = %s",
            data
        )
        # If no record was updated, then insert a new one
        if cursor.rowcount == 0:
            cursor.execute(
                "INSERT INTO assets (name, type, symbol) VALUES (%s, %s, %s)",
                data
            )
        conn.commit()


if __name__ == '__main__':  # pragma: no cover
    # Get tickers from the Coinbase API
    coins = top_30_crypto_pairs
    print(coins)

    # Connect to the database
    conn = connect_db()

    # Iterate over the tickers and update/create in the database
    for pair in coins:
        display_name = pair.replace("-", "/")
        symbol = pair

        update_or_create_asset(conn, display_name, symbol)
        print(f"Processing: {display_name} - {symbol}")

    conn.close()
    print("Database connection closed.")
