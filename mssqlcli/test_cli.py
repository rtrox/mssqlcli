"""MSSQL Cli Client written in python."""
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


import json

import mock

from click.testing import CliRunner

from mssqlcli import cli
from mssqlcli import test_fixtures

try:
    from StringIO import StringIO
except ImportError:  # pragma: nocover
    from io import StringIO


def test_split_param():
    """
    Test that split_param properly returns a list of params.

    In normal usage, this should be a single key/value pair
    split by a colon.
    """
    string = "last_name:Troxel"
    assert cli.split_param(string) == ["last_name", "Troxel"]


def test_split_param_with_strip():
    """
    Test that split_param properly returns a list of params.

    In normal usage, this should be a single key/value pair
    split by a colon.

    This test case ensures that spaces are properly stripped
    from split params.
    """
    string = "last_name:  Troxel"
    assert cli.split_param(string) == ["last_name", "Troxel"]


def test_render_template():
    """Test that jinja2 query templates are properly rendered."""
    query = StringIO(
        test_fixtures.get_file_contents('fake_template_query.sql')
    )
    query = cli.render_template(query, last_name="Troxel")
    assert query == "SELECT * FROM bogus_table WHERE last_name = Troxel;"


@mock.patch('pymssql.connect',
            side_effect=test_fixtures.MockPyMSSQLConnection)
def test_query_json(mock_connect):
    """Test query with basic options (json)."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        test_fixtures.populate_isolated_filesystem(
            'basic_config.yml',
            'fake_query.sql'
        )
        result = runner.invoke(
            cli.cli,
            ['-c', 'config.yml', '-o', 'json', 'query', 'query.sql']
        )
        assert result.exit_code == 0
        assert json.loads(result.output) == json.loads(
            test_fixtures.get_file_contents(
                'json_outputs/query_expected_json_output.json'
            )
        )
        assert mock_connect.called_with(
            'MY_MSSQL.example.com',
            'a_user',
            'a_password'
        )


@mock.patch('pymssql.connect',
            side_effect=test_fixtures.MockPyMSSQLConnection)
def test_query_csv(mock_connect):
    """Test query with CSV output."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        test_fixtures.populate_isolated_filesystem(
            'basic_config.yml',
            'fake_query.sql'
        )
        result = runner.invoke(
            cli.cli,
            ['-c', 'config.yml', '-o', 'csv', 'query', 'query.sql']
        )
        assert result.exit_code == 0
        assert result.output in [
            test_fixtures.get_file_contents(
                'csv_outputs/query_expected_csv_output.csv'
            ),
            test_fixtures.get_file_contents(
                'csv_outputs/query_expected_csv_output_2.csv'
            )
        ]
        assert mock_connect.called_with(
            'MY_MSSQL.example.com',
            'a_user',
            'a_password'
        )


@mock.patch('pymssql.connect',
            side_effect=test_fixtures.MockPyMSSQLConnection)
def test_query_default(mock_connect):
    """Test query with Pretty output."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        test_fixtures.populate_isolated_filesystem(
            'basic_config.yml',
            'fake_query.sql'
        )
        result = runner.invoke(
            cli.cli,
            ['-c', 'config.yml', 'query', 'query.sql']
        )
        assert result.exit_code == 0
        assert result.output in [
            test_fixtures.get_file_contents(
                'pretty_outputs/query_expected_pretty_output3'
            ),
            test_fixtures.get_file_contents(
                'pretty_outputs/query_expected_pretty_output4'
            )
        ]
        assert mock_connect.called_with(
            'MY_MSSQL.example.com',
            'a_user',
            'a_password'
        )


@mock.patch('pymssql.connect',
            side_effect=test_fixtures.MockPyMSSQLConnection)
def test_query_extended_config(mock_connect):
    """Test query with extended config."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        test_fixtures.populate_isolated_filesystem(
            'extended_config.yml',
            'fake_query.sql'
        )
        result = runner.invoke(
            cli.cli,
            ['-c', 'config.yml', 'query', 'query.sql']
        )
        assert result.exit_code == 0

        assert mock_connect.called_with(
            'MY_MSSQL.example.com',
            'a_user',
            'a_password',
            port=2345,
            timeout=10
        )


@mock.patch('pymssql.connect',
            side_effect=test_fixtures.MockPyMSSQLConnection)
def test_template_query_basic(mock_connect):
    """Test query with Pretty output."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        test_fixtures.populate_isolated_filesystem(
            'basic_config.yml',
            'fake_template_query.sql'
        )
        result = runner.invoke(
            cli.cli,
            ['-c', 'config.yml', '-o', 'pretty',
             'template_query', '-v', 'last_name:Troxel', 'query.sql']
        )
        assert result.exit_code == 0
        assert result.output in [
            test_fixtures.get_file_contents(
                'pretty_outputs/query_expected_pretty_output3'
            ),
            test_fixtures.get_file_contents(
                'pretty_outputs/query_expected_pretty_output4'
            )
        ]
        assert mock_connect.called_with(
            'MY_MSSQL.example.com',
            'a_user',
            'a_password'
        )
