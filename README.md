# fastapi-postgresql-boilerplate

A boilerplate that can serve as a base for FastAPI with postgresql

## Features

- [Poetry](https://python-poetry.org/docs/)
  > Dependency Management for Python
- [FastAPI](https://fastapi.tiangolo.com)
  > FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.
- [PostgreSQL](https://www.postgresql.org/docs)
  > PostgreSQL is an advanced, enterprise-class, and open-source relational database system.

## Requirements

- docker & docker-compose
- poetry

## Usage

### Install

```bash
### make .env file using .env.example file
$ cp .env.example .env

### To install the defined dependencies for project
$ poetry install
```

### Run

```bash
### running postgresql instance using docker-compose
$ docker-compose up postgresql -d

### To run FastAPI server
$ poetry run uvicorn app.main:app --host 0.0.0.0 --reload
```

### Test

```bash
### running postgresql instance using docker-compose
$ docker-compose up postgresql -d

### run test code
$ coverage run -m pytest -v
```

## Reference

-
