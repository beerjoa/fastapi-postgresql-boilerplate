# fastapi-postgresql-boilerplate

  [![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fbeerjoa%2Ffastapi-postgresql-boilerplate&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
  ![GitHub license](https://img.shields.io/github/license/beerjoa/fastapi-postgresql-boilerplate)
  ![GitHub issues](https://img.shields.io/github/issues/beerjoa/fastapi-postgresql-boilerplate)
  ![GitHub last commit](https://img.shields.io/github/last-commit/beerjoa/fastapi-postgresql-boilerplate)
  ![GitHub top language](https://img.shields.io/github/languages/top/beerjoa/fastapi-postgresql-boilerplate)


## Overview

🚀 FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python-type hints. \
I made and used this boilerplate for projects that I'm working on. 🧑‍💻 \
it was powerful for building data-driven applications using schema for data validation, serialization, and documentation. 📝


## Description

A boilerplate that can serve as a base for FastAPI with PostgreSQL \
Made with [FastAPI](https://fastapi.tiangolo.com), [PostgreSQL](https://www.postgresql.org/docs), [Docker](https://docs.docker.com), [Coverage](https://coverage.readthedocs.io/en/6.5.0/), [SQLAlchemy](https://docs.sqlalchemy.org/en/14/), [Pytest](https://docs.pytest.org/en/7.2.x/), [Black](https://black.readthedocs.io/en/stable/), [Flake8](https://flake8.pycqa.org/en/latest/), [Isort](https://pycqa.github.io/isort/),
and [Poetry](https://python-poetry.org/docs).

## Features

#### Developer experience

- 🐍 [Python 3.10](https://docs.python.org/3/) for programming language
- 🚀 [FastAPI](https://fastapi.tiangolo.com) for handling HTTP requests and responses
- 🐳 [Docker](https://docs.docker.com) for containerization
- 🐘 [PostgreSQL](https://www.postgresql.org/docs) for database
- 📦 [Poetry](https://python-poetry.org/docs) for dependency management
- 📈 [Coverage](https://coverage.readthedocs.io/en/6.5.0/) for code coverage
- 🧪 [Pytest](https://docs.pytest.org/en/7.2.x/) for unit and integration testing
- 💾 [SQLAlchemy](https://docs.sqlalchemy.org/en/14/) ORM for interacting with a database
- 🚧 [Flake8](https://flake8.pycqa.org/en/latest/) for linting
- 🎨 [Black](https://black.readthedocs.io/en/stable/) for code formatting
- 📚 [Isort](https://pycqa.github.io/isort/) for sorting imports

#### Back-end app features

- 🚫 JWT authentication for secure access to the API
- 🎢 Layered architecture. (Controller, Service, Repository, Model)
- 📦 Dependency injection for better code organization
- 📝 Swagger and Redoc for API documentation and testing
- ♻️ Schema validation for input and output data

## Requirements

- Python 3.10
- Poetry
- PostgreSQL
- Docker

## Getting Started
Every command below except `build` and `run` is executed in a docker container.


### Set Environment Variables

```bash
# Copy service env file
$ cp .env.example .env
# Copy db env file
$ cp .db.env.example .db.env
```

### Build and run the app with Docker Compose

```bash
# Build docker image
$ docker-compose build

# Run the app in the background
$ docker-compose up -d

# Watch logs
$ docker-compose logs -f

# Execute a command in a running container
$ docker-compose exec app <command>
```

### Migrate database 
before test or use the app, you need to migrate the database.
```bash
# init User table
$ docker-compose exec app poetry run alembic upgrade head
```

### Test

```bash
# Run unit tests using pytest
$ docker-compose exec app poetry run pytest
```

### Lint and format

```bash
# Run flake8
$ docker-compose exec app poetry run flake8

# Run black
$ docker-compose exec app poetry run black .

# Run isort
$ docker-compose exec app poetry run isort .
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.