"""Jsonification Functions for python-mssqlclient."""
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

import csv
import datetime
import json
import uuid

try:
    from StringIO import StringIO
except ImportError:  # pragma: nocover
    from io import StringIO


def stringify(obj):
    """
    Convert json non-serializable objects to string.

    Currently converts `datetime.datetime` objects.

    :param dict,list obj: object to be prepared for serialization.
    :rtype: dict,list
    """
    if type(obj) == list:
        iterable = enumerate(obj)
    if type(obj) == dict:
        iterable = obj.items()
    for k, v in iterable:
        if type(v) == datetime.datetime:
            obj[k] = str(v)

        if type(v) == uuid.UUID:
            obj[k] = str(v)

        if type(v) in [list, dict]:
            obj[k] = stringify(v)
    return obj


def jsonify(obj):
    """
    Convert serializable object to string.

    If Pygments is present, it will be used to colorify the json blob.
    :param list[dict] obj: object to be serialized.
    :returns: serialized json string.
    :rtype: string
    """
    formatted_json = json.dumps(stringify({"results": obj}), indent=4)

    try:
        from pygments import highlight, lexers, formatters
        colorful_json = highlight(
            formatted_json,
            lexers.JsonLexer(),
            formatters.TerminalFormatter()
        )
    except ImportError:
        return formatted_json

    return colorful_json


def csvify(obj):
    """
    Serialize object to CSV.

    :param list[dict] obj: list of dictionaries to be serialized.
    :returns: CSV serialized string.
    :rtype: string
    """
    output = StringIO()
    fieldnames = obj[0].keys()
    writer = csv.DictWriter(output, fieldnames=fieldnames)

    writer.writeheader()
    for item in stringify(obj):
        writer.writerow(item)
    out = output.getvalue()
    output.close()
    return out


def pretty_print(obj):
    """
    Serialize object to a pretty table.

    :param list[dict] obj: list of dictionaries to be serialized.
    :returns: PrettyTable string.
    :rtype: string
    """
    from prettytable import PrettyTable
    table = PrettyTable(obj[0].keys())
    for row in obj:
        table.add_row(row.values())
    return table.get_string()


FORMAT_OPTIONS = {
    "csv": csvify,
    "json": jsonify,
    "pretty": pretty_print
}
