from db import query_data, run_insert, bulk_insert
from wiki.create import fetch_wikipedia_pages_info

CHUNK_SIZE = 50
DELAY_SECONDS = 0.5

import time

# Yield successive n-sized
# chunks from l.
def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def add_associations(db_id, association_str):
    #print("add_associations(%s, %s)" % (db_id, association_str))
    params = {"entity_id": db_id, "association_str": association_str}
    run_insert("insert_association", params)


def process_new_entities(new_entities):
    #print(new_entities)

    for db_id in new_entities.keys():
        assocs = new_entities[db_id]

        association_str = ",".join([str(x.get('pageid')) for x in assocs])
        add_associations(db_id, association_str)

        cleaned_entities = list()
        for idx, a in enumerate(assocs):
            cleaned = {"pageid": a.get("pageid"), "title": a.get("title", "").replace("'", "''")}
            cleaned_entities.append(cleaned)

        bulk_insert("insert_entity", cleaned_entities)


def find_new_entities():
    entities = query_data("find_associations_to_populate")

    if not entities:
        print("No new entities to find!")
        return

    pages = dict()

    for e in entities:
        db_id = str(e.get('id'))
        wiki_id = str(e.get('wiki_id'))
        # name = e.get('name')

        pages[wiki_id] = db_id

    new_entities = dict()

    for chunk in divide_chunks([*pages], 4):
        pages_info = fetch_wikipedia_pages_info(chunk)
        for wiki_id in pages_info.keys():
            #print(pages_info.get(pi))
            new_entities[pages[str(wiki_id)]] = pages_info.get(wiki_id).get('associations')
        time.sleep(0.020)

    return new_entities

