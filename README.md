# StreetSide

A shared repository for street-side application

## Repository structure

Here are the main services that live in this repository:

- [StreetSide API](./street-side-api) - App's api, build with Python/FastAPI
- [StreetSide Frontend](./street-side-frontend) - React.js and Next.js front-end for the street side api interactions
- [StreetSide Web Scrapping Worker](./) - Worker to web scrap documents


## Contributing

#### Python env

The repository acts as a Python monorepo. To set up a flexible Python environment, we use [`mise`](https://github.com/jdx/mise) as our runtime manager i.e. as the tool that allows us to easily switch core dependency versions:
* see [`mise` quick start](https://mise.jdx.dev/getting-started.html#quickstart)
    * `sudo apt-get install mise && echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc`
* `mise use -g python@3.11`: this will add a `~/.config/mise/config.toml`. If locally, another Python version is needed, `mise use python@3.xx` can be used to override the global preferred version and this will add a `.mise.toml` file locally.

#### Python dependencies

Dependencies are managed with [`Poetry`](https://python-poetry.org/):
* `mise use -g poetry@1.6`: 
    * this is a community `mise` package and requires an approval
    * `poetry` will be based on the currently selected python version e.g. `poetry init` will use the currently selected Python version.

We rely on ["in project" virtualenvs](https://python-poetry.org/docs/configuration/#virtualenvsin-project) managed by poetry to make it easy to locate a project dependencies
```
poetry config virtualenvs.prefer-active-python true
poetry config virtualenvs.create true
poetry config virtualenvs.in-project true
```

These settings (stored in `~/.config/pypoetry/poetry.toml`) will apply globally and as a consequence, **we do not add `poetry.toml` in the repository**.

All project tools and dependencies can then be installed with:
* `poetry install [--all-extras]`

### Coding Style

Please read and follow the Python [PEP8 naming conventions](https://peps.python.org/pep-0008/#naming-conventions) and [recommendations](https://peps.python.org/pep-0008/#programming-recommendations)

### PR / Merge strategy

PRs are squashed and merged. This keeps the history clean: 1 PR = 1 idea = 1 commit on main.

### Commit Convention

#### Title

Use [Angular's commit convention](https://github.com/angular/angular/blob/master/CONTRIBUTING.md).

The following types are allowed:

- `build`: Changes that affect the build system or external dependencies
- `chore`: Changes that don't modify source code files
- `ci`: Changes to our CI configuration files and scripts
- `docs`: Documentation only changes
- `feat`: A new feature
- `fix`: A bug fix
- `perf`: A code change that improves performance
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `revert`: Reverts a previous commit
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
- `test`: Adding missing tests or correcting existing tests

#### Summary

Include a `Summary`. Describe the problem that the Pull Request is solving and how it is addressing it.

e.g:
```
This PR fixes this by doing that.
```

#### Test Plan

Include a `Test Plan`. A Test plan includes the steps taken to ensure the code does what it's supposed to do.
Sometimes e.g. when refactoring, this would be be relying on existing tests, sometimes we may have some manual test phase.
The goal is to write down those steps so that:

- reviewers have confidence in the fact that the code works
- there remains some documentation how to reproduce the test

Including screenshots can sometimes be a good idea.

e.g:
```
Test Plan:
- updated tests with the following test case: assert that if X is given then Y is produced
```

```
Test Plan:
- ran the command locally with the following flags .., then checked in the console that output X was present: <screenshot attached>
```
