#!/usr/bin/env python3

from dotenv import load_dotenv
import os
from pathlib import Path
import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def establish_connection(host, port, admin_user, admin_password):
    conn = psycopg2.connect(
        host=host,
        port=port,
        user=admin_user,
        password=admin_password,
        database='postgres'
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
    print(f"Configuring user settings...")
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


def create_and_setup(db_name, db_user, db_password,
                     host, port,
                     admin_user, admin_password):
    conn = establish_connection(
        host,
        port,
        admin_user,
        admin_password
    )
    cursor = conn.cursor()

    create_user(cursor, db_user, db_password)
    create_db(cursor, db_name)
    configure_settings(cursor, db_user)
    grant_db_priviligies(cursor, db_name, db_user)

    cursor.close()
    conn.close()


def grant_public_schema_access(db_user, host, port,
                               admin_user, admin_password):
    conn = establish_connection(
        host,
        port,
        admin_user,
        admin_password
    )
    cursor = conn.cursor()

    cursor.execute(
        sql.SQL("GRANT ALL ON SCHEMA public TO {}").format(
            sql.Identifier(db_user)
        )
    )

    cursor.close()
    conn.close()


def create_and_setup_database(db_name, db_user, db_password, admin_password,
                              admin_user='postgres', host='localhost', port=5433):
    try:
        create_and_setup(db_name, db_user, db_password,
                         host, port,
                         admin_user, admin_password)

        grant_public_schema_access(db_user, host, port,
                                   admin_user, admin_password)

        print(f"Success! Database '{db_name}' and user '{db_user}' are ready.")

    except psycopg2.Error as e:
        print(f"Error occured: {e}")
        exit(1)


def get_password(key):
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(dotenv_path=env_path)
    password = os.getenv(key)

    if not password:
        print(f"No password found by key {key}")
        exit(1)
    return password


def main():
    try:
        create_and_setup_database(
            db_name='travelmap',
            db_user='travelmap_user',
            db_password=get_password("DB_PASSWORD"),
            admin_password=get_password("DB_ADMIN_PASSWORD")
        )
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        exit(1)


if __name__ == "__main__":
    main()
