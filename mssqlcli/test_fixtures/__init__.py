"""Testing Fixtures for MSSQL-CLI."""
# Copyright (C) 2016 Russell Troxel

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os

from datetime import datetime

FIXTURES_PATH = os.path.dirname(os.path.realpath(__file__))


def get_file_contents(filename):
    """Retrieve contents of file in this directory."""
    filepath = os.path.join(FIXTURES_PATH, filename)
    with open(filepath, 'r') as f:
        return f.read()


def populate_isolated_filesystem(configfile, queryfile):
    """
    Create a config file and query for testing.

    Helper function uses files in this directory to populate a
    `click.isolated_filesystem()`.
    """
    with open('config.yml', 'w') as f:
        f.write(get_file_contents(configfile))
    with open('query.sql', 'w') as f:
        f.write(get_file_contents(queryfile))


def mock_execute_query(config, query):
    """
    Mock the mssqlcli.drivers.mssql.execute_many method.

    Executing a query will return a static result set.
    """
    return [
        {"a": "one", "b": "two"},
        {"a": "three", "b": datetime(2016, 10, 20, 21, 10, 36, 621341)}
    ]


class MockPyMSSQLCursor(object):
    """
    Mocks pymssql.Cursor.

    Mock object to be returned by MockPyMSSQLConnection.cursor().
    """

    def __init__(self, as_dict=False):
        """Mock out as_dict option, as this is the only one we use."""
        self.as_dict = as_dict
        self.results = []

    def __iter__(self):
        """Make cursor iterable to simulate a real cursor."""
        return iter(self.results)

    def execute(self, query):
        """
        Mock the pymssql.Cursor.execute method.

        Executing a query will return a static result set.
        """
        self.results = [
            {"a": "one", "b": "two"},
            {"a": "three", "b": datetime(2016, 10, 20, 21, 10, 36, 621341)}
        ]


class MockPyMSSQLConnection(object):
    """
    Mocks pymssql.connection.

    To be used with mock as return value for pymssql.connect().
    """

    def __init__(self, server, username, password, **kwargs):
        """
        Mock the pymssql.Connection.

        Utilizes server, username, password, the standard options for a
        Connection.
        """
        self.server = server
        self.username = username
        self.password = password

    def cursor(self, as_dict=False):
        """Dummy method to create a fake cursor."""
        return MockPyMSSQLCursor(as_dict)
