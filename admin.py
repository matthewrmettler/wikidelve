from db.create import create_database, seed_database
from db.populate import find_new_entities, process_new_entities

RESET_DATABASE = False

NUM_RUNS = 10
def update_database():
    for i in range(NUM_RUNS):
        new_entities = find_new_entities()
        process_new_entities(new_entities)


def main():
    if RESET_DATABASE:
        create_database()
        seed_database()

    update_database()


if __name__ == "__main__":
    main()
