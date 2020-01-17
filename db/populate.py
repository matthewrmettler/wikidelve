from db import query_data
from wiki.create import fetch_wikipedia_pages_info


def find_new_entities():
    entities = query_data("find_associations_to_populate")

    if not entities:
        print("No new entities to find!")
        return

    pages = dict()

    for e in entities:
        db_id = str(e.get('id'))
        wiki_id = str(e.get('wiki_id'))
        name = e.get('name')

        pages[wiki_id] = db_id

    pages_info = fetch_wikipedia_pages_info([*pages])

    for pi in pages_info.keys():
        print(pages_info.get(pi))
