from db.create import create_database, seed_database
from db.populate import find_new_entities

RESET_DATABASE = True


def update_database():
    find_new_entities()


def main():
    if RESET_DATABASE:
        create_database()
        seed_database()

    update_database()


if __name__ == "__main__":
    main()
