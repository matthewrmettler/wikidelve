from db import create_database, test_database

from wiki.create import fetch_wikipedia_pages_info

def test():
    page_ids = ["307"]
    results = fetch_wikipedia_pages_info(page_ids)

    for k in results:
        print(k)


def main():
    #create_database()
    #test_database()
    test()

if __name__ == "__main__":
    main()