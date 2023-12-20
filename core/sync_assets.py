import psycopg2
import sys
from config_loader import load_config
from Historic_Crypto import Cryptocurrencies

def connect_db():
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

def update_or_create_asset(conn, name, symbol='$', asset_type='x'):
    # Create a cursor
    with conn.cursor() as cursor:
        # Store the data in a variable
        data = (name, asset_type, symbol[:9])

        # First, try to update the existing record
        cursor.execute(
            "UPDATE public.assets SET name = %s, type = %s WHERE symbol = %s",
            data
        )
        # If no record was updated, then insert a new one
        if cursor.rowcount == 0:
            cursor.execute(
                "INSERT INTO public.assets (name, type, symbol) VALUES (%s, %s, %s)",
                data
            )
        conn.commit()


if __name__ == '__main__':
    # Get tickers from the Coinbase API
    coins = Cryptocurrencies().find_crypto_pairs()
    coins = coins[coins['status'] != 'delisted']
    print(coins)

    # Connect to the database
    conn = connect_db()

    # Iterate over the tickers and update/create in the database
    for index, row in coins.iterrows():
        display_name = row['display_name']
        symbol = row['id']
        print(f"Processing: {display_name} - {symbol}")
        update_or_create_asset(conn, display_name, symbol)

    conn.close()
    print("Database connection closed.")
