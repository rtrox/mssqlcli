# Contributing

MS-SQL CLI is an open-source project, hosted [on GitHub][1]. All Contributors
are welcome, a current list of open issues is available [here][2].

## Development Environment

No additional dependencies are required for development, simply follow the
standard installation instructions from README.md. I recommend that you use
`python setup.py develop`, rather than `install` to allow quick code changes.

## Testing

To test your code prior to submission, simply:

```bash
python setup.py test
```

This will ensure that tox and virtualenv are installed, and then run the test
suite against the interpreters available locally.

## Acceptance Criteria

### Pull requests should be made against the `develop` branch.
This repository utilizes git-flow for the most part. as such, new PRs should be
made against the `develop` branch. Changes will be merged from `develop` into
master during releases.

### Pull requests should follow full pep8 guidelines (the above testing will verify this).

### Pull requests should have thought-out test cases for any new code.
Test Coverage is currently at 100%. Pull requests should not reduce this
coverage, and should contain thought out test cases for new code.

### Pull requests should contain only a single commit (please squash commits prior to submitting Pull Request)
Pull Requests will be merged via rebase, as we use gitchangelog to generate
changelogs. As such, The commit message in your pull request should describe
what is being changed, and should follow the gitchangelog commit message
specs (below).

### Pull request commit messages should follow GitChangeLog specifications
These specifications can be found [here][3].


As an example, if I was fixing documentation, I might create the following commit text:

```fix: doc: Fixed Installation Instructions to reference proper pip package.```


The above requirements are verified via Travis-CI and Coveralls for Python versions 2.7, 3.4, and 3.5.


[1]: https://github.com/rtrox/mssqlcli
[2]: https://github.com/rtrox/mssqlcli/issues
[3]: https://github.com/vaab/gitchangelog/blob/master/gitchangelog.rc.reference
