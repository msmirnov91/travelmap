#!/usr/bin/env python3

import os
import sys
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from utils.env_utils.load_env import load_env_vars


def establish_connection(host, port, admin_user, admin_password, database):
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=admin_user,
        password=admin_password,
        database=database
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    return conn


def create_user(cursor, db_user, db_password):
    cursor.execute("""
            SELECT 1 FROM pg_roles WHERE rolname = %s
        """, (db_user,))

    if cursor.fetchone():
        print(f"User '{db_user}' already exists, updating password...")
        query = sql.SQL("ALTER USER {} WITH PASSWORD %s")
    else:
        print(f"Creating user '{db_user}'...")
        query = sql.SQL("CREATE USER {} WITH PASSWORD %s")

    cursor.execute(query.format(sql.Identifier(db_user)), (db_password,))


def create_db(cursor, db_name):
    cursor.execute("""
            SELECT 1 FROM pg_database WHERE datname = %s
    """, (db_name,))

    if cursor.fetchone():
        print(f"Database '{db_name}' already exists")
    else:
        print(f"Creating database '{db_name}'...")
        cursor.execute(
            sql.SQL("CREATE DATABASE {}").format(
                sql.Identifier(db_name)
            )
        )


def configure_settings(cursor, db_user):
    print("Configuring user settings...")
    query = sql.SQL("""
        ALTER ROLE {} SET client_encoding TO 'utf8';
        ALTER ROLE {} SET default_transaction_isolation TO 'read committed';
        ALTER ROLE {} SET timezone TO 'UTC';
    """).format(sql.Identifier(db_user), sql.Identifier(db_user), sql.Identifier(db_user))
    cursor.execute(query)


def grant_db_priviligies(cursor, db_name, db_user):
    cursor.execute(
        sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(
            sql.Identifier(db_name),
            sql.Identifier(db_user)
        )
    )


def create_db_and_user():
    conn = establish_connection(
        host=get_from_env("DB_HOST"),
        port=int(get_from_env("DB_PORT")),
        admin_user=get_from_env("DB_ADMIN_USER"),
        admin_password=get_from_env("DB_ADMIN_PASSWORD"),
        database='postgres'
    )
    cursor = conn.cursor()

    db_name = get_from_env("DB_NAME")
    db_user = get_from_env("DB_USER")
    db_password = get_from_env("DB_PASSWORD")

    create_user(cursor, db_user, db_password)
    create_db(cursor, db_name)
    configure_settings(cursor, db_user)
    grant_db_priviligies(cursor, db_name, db_user)

    cursor.close()
    conn.close()


def turn_on_postgis(cursor):
    print("Turning on PostGIS...")
    cursor.execute("""
            SELECT extname, extversion FROM pg_extension WHERE extname = 'postgis';
    """)
    if cursor.fetchone():
        print("PostGIS already turned on")
    else:

        query = """
        CREATE EXTENSION postgis;
        CREATE EXTENSION postgis_topology;
        """
        cursor.execute(query)
        print("PostGIS turned on successfully")


def configure_created_db():
    conn = establish_connection(
        host=get_from_env("DB_HOST"),
        port=int(get_from_env("DB_PORT")),
        admin_user=get_from_env("DB_ADMIN_USER"),
        admin_password=get_from_env("DB_ADMIN_PASSWORD"),
        database=get_from_env("DB_NAME")
    )
    cursor = conn.cursor()

    db_user = get_from_env("DB_USER")

    cursor.execute(
        sql.SQL("GRANT ALL ON SCHEMA public TO {}").format(
            sql.Identifier(db_user)
        )
    )
    turn_on_postgis(cursor)

    cursor.close()
    conn.close()


def get_from_env(key):
    value = os.getenv(key)
    if not value:
        print(f"No value found by key {key}")
        sys.exit(1)
    return value


def main():
    load_env_vars()

    try:
        create_db_and_user()
        configure_created_db()

        db_name = get_from_env("DB_NAME")
        db_user = get_from_env("DB_USER")
        print(f"Success! Database '{db_name}' and user '{db_user}' are ready.")

    except psycopg2.Error as e:
        print(f"Error occured: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
