# Ham Dash

![Lint & Test](https://github.com/jamescurtin/ham-dash/workflows/Lint%20&%20Test/badge.svg)
![codecov](https://codecov.io/gh/jamescurtin/ham-dash/branch/main/graph/badge.svg)


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

and go to http://localhost:8000

## Updating Dependencies

Requirements should be re-locked every time dependencies in `pyproject.toml` are updated.
Images should then be re-built to include the new dependencies.

```bash
docker-compose run --rm lock-requirements
docker-compose run build
```

## Testing & Linting

Should be run locally before pushing, and are validated by Github Actions.
Tests will fail if unit test coverage is less than 95%.

```bash
docker-compose run --rm lint
docker-compose run --rm test
```
