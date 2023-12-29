"""Tests for script `core.sync_assets`."""
import unittest
from unittest.mock import patch, MagicMock, call

from psycopg2 import OperationalError
from core.sync_assets import connect_db, update_or_create_asset


class TestDatabaseConnection(unittest.TestCase):
    """
    Test for check the database connection.

    Using the mock library, we can mock the psycopg2.connect function
    to return a MagicMock object. This allows us to test the connect_db
    function without actually connecting to the database.

    And the load config function is mocked to return a dictionary of
    database connection settings. This allows us to test the connect_db
    function without loading the settings from the .env file.
    """

    @patch('core.sync_assets.load_config')
    @patch('core.sync_assets.psycopg2.connect')
    def test_connect_db_success(self, mock_connect, mock_load_config):
        """Test successful database connection."""
        mock_load_config.return_value = {
            'DBNAME': 'testdb',
            'DBUSER': 'testuser',
            'DBPASSWORD': 'testpass',
            'DBHOST': 'localhost',
            'DBPORT': '5432'
        }

        # Config the mock so that pyscopg2.connect
        mock_connect.return_value = MagicMock()

        # Call the function and verify that
        conn = connect_db()
        self.assertIsNotNone(conn)

    @patch('core.sync_assets.load_config')
    @patch('core.sync_assets.psycopg2.connect')
    def test_connect_db_failure(self, mock_connect, mock_load_config):
        """Test database connection failure."""
        mock_load_config.return_value = {
            'DBNAME': 'testdb',
            'DBUSER': 'testuser',
            'DBPASSWORD': 'testpass',
            'DBHOST': 'localhost',
            'DBPORT': '5432'
        }

        # Config the mock so that psycopg2.connect raises an exception
        mock_connect.side_effect = OperationalError

        # Call the function and verify that SystemExit is raised
        with self.assertRaises(SystemExit):
            connect_db()


class TestUpdateOrCreateAsset(unittest.TestCase):
    """Tests for Update Or Create function."""

    def setUp(self):
        """Set up method to initialize the test case."""
        # Simulate a db conn, a cursor and assign the cursor to the conn
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()

        self.mock_conn.cursor.return_value.__enter__.return_value = \
            self.mock_cursor

    def test_update_existing_asset(self):
        """Test updating an existing asset record."""
        # Config the mock indicating that a record was updated
        self.mock_cursor.rowcount = 1

        update_or_create_asset(self.mock_conn, 'Test Asset', 'TA', 'crypto')

        # Check that execute was called with the update query
        self.mock_cursor.execute.assert_called_once_with(
            "UPDATE assets SET name = %s, type = %s, price = %s, volume = %s \
                WHERE symbol = %s",
            ('Test Asset', 'TestType', 'TestPrice', 'TestVolume', 'TestSymbol')
        )

    def test_create_new_asset(self):
        """Test creating a new asset record."""
        # Config the mock indicating that no record was updated
        self.mock_cursor.rowcount = 0

        update_or_create_asset(self.mock_conn, 'New Asset','TestPrice',
                               'TestVolume', 'TestSymbol', 'TestType')

        # Check that execute was called in order (update, then insert)
        calls = [
            call(
                "UPDATE assets SET name = %s, type = %s, price = %s,\
                    volume = %s WHERE symbol = %s",
                ('New Asset', 'TestType', 'TesPrice', 'TestVolume',
                 'TestSymbol')
            ),
            call(
                "INSERT INTO assets (name, type, price, volume, symbol) \
                VALUES (%s, %s, %s, %s, %s)",
                ('New Asset', 'TestType', 'TesPrice', 'TestVolume',
                  'TestSymbol')
            )
        ]
        self.mock_cursor.execute.assert_has_calls(calls, any_order=False)
