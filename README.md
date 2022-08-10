# fastapi-postgresql-boilerplate

[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fbeerjoa%2Ffastapi-postgresql-boilerplate&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

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
