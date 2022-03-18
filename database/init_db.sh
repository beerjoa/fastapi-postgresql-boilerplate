#!/bin/bash
set -e

echo "  Creating user and database '$DEFAULT_DATABASE'  "
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER $DEFAULT_DATABASE;
    CREATE DATABASE $DEFAULT_DATABASE;
    GRANT ALL PRIVILEGES ON DATABASE $DEFAULT_DATABASE TO $DEFAULT_DATABASE;

    \connect $DEFAULT_DATABASE

    CREATE TABLE IF NOT EXISTS users (
        id serial PRIMARY KEY,
        name VARCHAR ( 50 ) UNIQUE NOT NULL,
        password VARCHAR ( 50 ) NOT NULL,
        email VARCHAR ( 255 ) UNIQUE NOT NULL,
        created_on TIMESTAMP NOT NULL,
        last_login TIMESTAMP 
    );
EOSQL