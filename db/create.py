from db import DATABASE_NAME, execute_query


def create_database():
    with open(DATABASE_NAME, 'w') as f:
        pass
    execute_query("database_creation")


def seed_database():
    execute_query("database_seeding")
