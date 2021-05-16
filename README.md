# Ham Dash

![Lint & Test](https://github.com/jamescurtin/ham-dash/workflows/Lint%20&%20Test/badge.svg)
[![codecov](https://codecov.io/gh/jamescurtin/ham-dash/branch/main/graph/badge.svg?token=zmg1twfMd1)](https://codecov.io/gh/jamescurtin/ham-dash)
[![license](https://img.shields.io/github/license/jamescurtin/ham-dash.svg)](https://github.com/jamescurtin/ham-dash/blob/main/LICENSE)

TODO: Summary

## Running

Copy `.env.example` to `.env` and replace the placeholders with real values.

To run in development mode (with auto-reloading):

```bash
docker-compose up backend-dev
```

To run in production mode:

```bash
docker-compose up backend
```

and go to [http://localhost:8000](http://localhost:8000)

## Modifying Dependencies

Use `poetry` to update dependencies, instead of modifying `pyproject.toml`
directly. This can be done using the `poetry` service in `docker-compose.yaml`.
Images should then be re-built to include the updated dependencies.

Add a dependency

```bash
docker-compose run --rm poetry add <SOME-DEPENDENCY>
docker-compose build
```

## Testing & Linting

Should be run locally before pushing, and are validated by Github Actions.
Tests will fail if unit test coverage is less than 95%.

```bash
docker-compose run --rm lint
docker-compose run --rm test
```
