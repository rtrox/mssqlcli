"""MS-SQL CLI: a Python command line interface for Microsoft SQL Server."""
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

import click

from mssqlcli import __version__, formats
from mssqlcli.config import Config
from mssqlcli.drivers.mssql import execute_query


def split_param(string, sep=":"):
    """Split a key/value parameter by separator."""
    split = string.split(sep)
    for idx, item in enumerate(split):
        split[idx] = item.strip()
    return split


def render_template(query, **kwargs):
    """Helper function to render jinja templated queries."""
    from jinja2 import Template
    return Template(query.read()).render(**kwargs)


@click.group()
@click.version_option(__version__, prog_name=__doc__.strip("."))
@click.option("--config-file", "-c", type=click.Path(),
              default=os.path.expanduser("~/.config/mssqlcli.yml"),
              help=("Override default config file location"
                    " (default: ~/.config/pymssql.yml)."))
@click.option("--output", "-o",
              type=click.Choice(formats.FORMAT_OPTIONS.keys()),
              default="pretty")
@click.pass_context
def cli(ctx, config_file, output):
    """Placeholder Function for click group."""
    # RTrox: Currently there is only command. This layout is
    # to allow forward compatibility once a `configure`
    # option is added, as well as any other future commands
    # that may be needed for MS-SQL Administration.
    if ctx.obj is None:
        ctx.obj = {}

    ctx.obj['config'] = Config(config_file)
    ctx.obj['output_formatter'] = formats.FORMAT_OPTIONS[output]


@click.argument("query", type=click.File('r'))
@cli.command()
@click.pass_context
def query(ctx, query):
    """
    Run a query against an MS-SQL Database.

    Config-file must be created before the query will succeed.
    Example configs can be found in the README.md.

    :param string config_file: path to config file. (yaml)
    :param string output: output type. Choices: pretty,json,csv
    :param string query: location of query file to be ran against the server.
    :rtype: None

    """
    query = query.read()

    results = execute_query(ctx.obj['config'], query)
    output = ctx.obj['output_formatter'](results)
    click.echo(output)


@click.option("--variable", "-v", multiple=True,
              help=('Variable for substitution in template. ex:'
                    '"-v first_name:russell" to replace {{ first_name }}')
              )
@click.argument("query", type=click.File('r'))
@cli.command()
@click.pass_context
def template_query(ctx, variable, query):
    """Run Jinga2 templated query on an MS-SQL Database"""
    kwargs = {}
    for v in variable:
        v = split_param(v)
        kwargs[v[0]] = v[1]

    query = render_template(query, **kwargs)

    results = execute_query(ctx.obj['config'], query)
    output = ctx.obj['output_formatter'](results)
    click.echo(output)


if __name__ == "__main__":  # pragma: nocover
    cli()
