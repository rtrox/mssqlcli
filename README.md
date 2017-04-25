# MS-SQL Command Line Interface (mssqlcli)

[![PyPI](https://img.shields.io/pypi/v/mssqlcli.svg)](https://pypi.python.org/pypi/mssqlcli)
[![Build Status](https://img.shields.io/travis/rtrox/mssqlcli/master.svg)](https://travis-ci.org/rtrox/mssqlcli)
[![Coverage Status](https://img.shields.io/coveralls/rtrox/mssqlcli/master.svg)](https://coveralls.io/github/rtrox/mssqlcli?branch=master)

MS-SQL CLI is a unix command line tool for accessing and running arbitrary
queries against an Microsoft SQL database.


## Binary Dependencies

- [FreeTDS][1] - Binary Library providing access to MSSQL and Sybase DBs.



## Installation

1. Install the FreeTDS Library
    - Debian/Ubuntu: `sudo apt-get install freetds-dev`
    - Mac OSX: `brew install freetds`
2. Install mssqlcli
    - `pip install mssqlcli`
*OR*
    -  Clone and  `python setup.py install`

### DB_VERSION_80 Errors during Installation (OS X)

On Mac OS X, there is a bug with `pymssql` v2.1.2 which may cause this error:
```bash
error: use of undeclared identifier 'DBVERSION_80'
```
If you see this error, simply install the latest version of `pymssql` from git prior to installation of mssqlcli:
```bash
pip install -e git+https://github.com/pymssql/pymssql.git#egg=pymssql-2.1.2
```


## Configuration

Configuration is handled with a single YAML configuration file, located by
default at `~/.config/mssqlcli.yml`.

Example Config:
```yaml
keyring_app_name: another_app # Optional, defaults to mssqlcli
username: USE_KEYRING("global:LDAPUser")
password: USE_KEYRING("global:LDAP")
# OR
# username: my_plaintext_username
# password: my_plaintext_password
server: MY_MSSQL.example.com

# The below is optional, and should be used if
# Windows Auth will be used instead of MSSQL Auth.
windows_authentication: true
domain: MY_DOMAIN
```


## Usage

```bash
~ [ mssqlcli --help Usage: mssqlcli [OPTIONS] COMMAND [ARGS]...

Options:
  --version  Show the version and exit.
  -c, --config-file PATH   Override default config file location
                           (default: ~/.config/pymssql.yml).
  -o, --output [json|csv|pretty]
  --help  Show this message and exit.

Commands:
  query           Run a query against an MS-SQL Database.
  template_query

~ [ mssqlcli query --help
Usage: mssqlcli query [OPTIONS] QUERY

Options:
  --help                   Show this message and exit.

~ [ mssqlcli template_query --help
Usage: mssqlcli template_query [OPTIONS] QUERY

Options:
  -v, --variable TEXT   Variable for substitution in template. ex:"-v
                        first_name:russell" to replace {{ first_name }}
  --help                Show this message and exit.
```


## Examples
The general usage model is to store your SQL queries in flat files, and
access them with the CLI client. Personally, I store my queries in
~/sql_queries.


Run Query and return results as a json blob
```bash
mssqlcli query {path to query}.sql
```

Run query and return results in CSV format
```bash
mssqlcli -o csv query {path to query}.sql
```

Redirect csv to File
```bash
mssqlcli -o csv query {path to query}.sql > results.csv
```

Run query and return results as a json blob
```bash
mssqlcli -o json query  {path to query}.sql
```

Send a template query to the server in file {path to query}.sql.
```bash
mssqlcli template_query -v 'last_name: Ugur' {path to query}.sql
```

### Template Queries
An example of a templated SQL query is also given below. These are
the kind of queries that can be used alongside template_query command.
```bash
SELECT * FROM bogus_db.users WHERE last_name = '{{ last_name }}';
```


[1]: http://www.freetds.org/
[2]: http://pymssql.org/en/stable/
[3]: http://click.pocoo.org/5/
[4]: https://github.com/pymssql/pymssql/issues/432
