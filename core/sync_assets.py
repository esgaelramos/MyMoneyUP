"""
Script to sync assets from the Historic Crypto Library to the database.

This script uses the Historic Crypto Library to get the list of assets
from the Coinbase API and syncs them to the database.

Example:
    python core/sync_assets.py
"""
import sys

import psycopg2
from psycopg2.extensions import connection
from Historic_Crypto import Cryptocurrencies
from config_loader import load_config

import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def scrape_data(days_ago):
    crypto_date_list = []
    crypto_name_list = []
    crypto_symbol_list = []
    crypto_market_cap_list = []
    crypto_price_list = []
    crypto_circulating_supply_list = []
    crypto_voulume_24hr_list = []
    crypto_pct_1hr_list = []
    crypto_pct_24hr_list = []
    crypto_pct_7day_list = []
    previous_date = datetime.now() + timedelta(days=-days_ago)
    date = previous_date.strftime('%Y%m%d')
    url = 'https://coinmarketcap.com/historical/' + str(date)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tr = soup.find_all('tr', attrs={'class': 'cmc-table-row'})
    count = 0
    for row in tr:
        if count == 50:
            break
        count += 1

        try:
            crypto_date = date
        except AttributeError:
            crypto_date = None

        try:
            name_column = row.find('td', attrs={'class': 'cmc-table__cell cmc-table__cell--sticky cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__name'})
            crypto_name = name_column.find('a', attrs={'class': 'cmc-table__column-name--name cmc-link'}).text.strip()
        except AttributeError:
            crypto_name = None

        try:
            crypto_symbol = row.find('td', attrs={'class': 'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__symbol'}).text.strip()
        except AttributeError:
            crypto_symbol = None

        try:
            crypto_market_cap = row.find('td', attrs={'class': 'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__market-cap'}).text.strip()
        except AttributeError:
            crypto_market_cap = None

        try:
            crypto_price = row.find('td', attrs={'class': 'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price'}).text.strip()
        except AttributeError:
            crypto_price = None

        try:
            crypto_circulating_supply = row.find('td', attrs={'class': 'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__circulating-supply'}).text.strip().split(' ')[0]
        except AttributeError:
            crypto_circulating_supply = None

        try:
            crypto_voulume_24hr_td = row.find('td', attrs={'class': 'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__volume-24-h'})
            crypto_voulume_24hr = crypto_voulume_24hr_td.find('a', attrs={'class': 'cmc-link'}).text.strip()
        except AttributeError:
            crypto_voulume_24hr = None

        try:
            crypto_pct_1hr = row.find('td', attrs={'class': 'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-1-h'}).text.strip()
        except AttributeError:
            crypto_pct_1hr = None

        try:
            crypto_pct_24hr = row.find('td', attrs={'class': 'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-24-h'}).text.strip()
        except AttributeError:
            crypto_pct_24hr = None

        try:
            crypto_pct_7day = row.find('td', attrs={'class': 'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__percent-change-7-d'}).text.strip()
        except AttributeError:
            crypto_pct_7day = None
        crypto_date_list.append(crypto_date)
        crypto_name_list.append(crypto_name)
        crypto_symbol_list.append(crypto_symbol)
        crypto_market_cap_list.append(crypto_market_cap)
        crypto_price_list.append(crypto_price)
        crypto_circulating_supply_list.append(crypto_circulating_supply)
        crypto_voulume_24hr_list.append(crypto_voulume_24hr)
        crypto_pct_1hr_list.append(crypto_pct_1hr)
        crypto_pct_24hr_list.append(crypto_pct_24hr)
        crypto_pct_7day_list.append(crypto_pct_7day)
    return (
        crypto_date_list, crypto_name_list, crypto_symbol_list,
        crypto_market_cap_list, crypto_price_list,
        crypto_circulating_supply_list, crypto_voulume_24hr_list,
        crypto_pct_1hr_list, crypto_pct_24hr_list, crypto_pct_7day_list
    )





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
        data = (name, asset_type, symbol)

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



better_40 = Cryptocurrencies(extended_output=True).find_crypto_pairs()
print(better_40)
conditions = "(status == 'online') & (fx_stablecoin == False) & (trading_disabled == False)"
better_40 = better_40.query(conditions)
print(better_40)
monedas_excluidas = ['EUR', 'GBP', 'DAI', 'USDT', 'USDC','BTC', 'ETH']
filtered_currency = better_40[~better_40['quote_currency'].isin(monedas_excluidas)]


if __name__ == '__main__':
      
      
    (
        crypto_date_list, crypto_name_list, crypto_symbol_list,
        crypto_market_cap_list, crypto_price_list,
        crypto_circulating_supply_list, crypto_voulume_24hr_list,
        crypto_pct_1hr_list, crypto_pct_24hr_list, crypto_pct_7day_list
    ) = scrape_data(60)
    
    df = pd.DataFrame({
        'Date': crypto_date_list,
        'Name': crypto_name_list,
        'Symbol': crypto_symbol_list,
        'Market Cap': crypto_market_cap_list,
        'Price': crypto_price_list,
        'Circulating Supply': crypto_circulating_supply_list,
        'Volume (24hr)': crypto_voulume_24hr_list,
        '% 1h': crypto_pct_1hr_list,
        '% 24h': crypto_pct_24hr_list,
        '% 7d': crypto_pct_7day_list
    })

    df['Market Cap'] = df['Market Cap'].str.replace('[$,]', '', regex=True)
    df['Price'] = df['Price'].str.replace('[$,]', '', regex=True)

    # Replace the commas (,) from the 'Circulating Supply' column
    df['Circulating Supply'] = df['Circulating Supply'].str.replace(',', '')

    # Replace the dollar signs ($) and commas (,) from the 'Volume (24hr)' columns
    df['Volume (24hr)'] = df['Volume (24hr)'].str.replace('[$,]', '', regex=True)

    # Replace the unchange sign (--), the smaller sign (<), the larger sign (>) and percentage sign (%) from the '% 1h', '% 24h', and '% 7d' columns
    df['% 1h'] = df['% 1h'].str.replace('--', '0').str.lstrip('>').str.lstrip('<').str.rstrip('%')
    df['% 24h'] = df['% 24h'].str.replace('--', '0').str.lstrip('>').str.lstrip('<').str.rstrip('%')
    df['% 7d'] = df['% 7d'].str.replace('--', '0').str.lstrip('>').str.lstrip('<').str.rstrip('%')

    # Convert the numeric columns to appropriate data types, replacing invalid values with NaN
    numeric_cols = ['Market Cap', 'Price', 'Circulating Supply', 'Volume (24hr)', '% 1h', '% 24h', '% 7d']
    df[numeric_cols] = df[numeric_cols].apply(lambda x: pd.to_numeric(x))

    # Handle specific case of "<0.01" by replacing it with a small non-zero value, e.g., 0.005
    df.loc[df['% 1h'] < 0, '% 1h'] = 0.005

    # Set the display format for float and integer values
    pd.options.display.float_format = '{:.2f}'.format
    merged_df = pd.merge(df, filtered_currency, left_on='Symbol', right_on='base_currency', how='left')
    merged_df['quote_currency'] = 'USD'
    merged_df['display_name'] = merged_df['Symbol'] + '/' + merged_df['quote_currency']
    merged_df['id'] = merged_df['Symbol'] + '-' + merged_df['quote_currency']
    print(merged_df)
    top_cryptos = merged_df.nlargest(40, 'Market Cap')
    top_cryptos = top_cryptos.dropna()

    # Connect to the database
    conn = connect_db()

    # Iterate over the tickers and update/create in the database
    for index, row in top_cryptos.iterrows():
        display_name = row['display_name']
        symbol = row['id']

        update_or_create_asset(conn, display_name, symbol)
        print(f"Processing: {display_name} - {symbol}")

    conn.close()
    print("Database connection closed.")
