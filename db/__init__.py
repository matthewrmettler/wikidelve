import sqlite3

DATABASE_NAME = "test.db"

# https://stackoverflow.com/a/9538363
def dict_from_sqlite3_row(row):
    return dict(zip(row.keys(), row))


def load_query(query_name):
    try:
        with open("db/queries/{}.sql".format(query_name), 'r') as f:
            sql_file = f.read()
            commands = sql_file.split(';')
            return commands
    except Exception as e:
        print("Could not load query %s! Error: %s" % (query_name, e))
        return ""


def execute_query(query_name):
    print("execute_query(%s)" % query_name)
    query_array = load_query(query_name)
    #print(query_array)
    conn = sqlite3.connect(DATABASE_NAME)
    c = conn.cursor()
    for q in query_array:
        c.execute(q)
    conn.commit()
    conn.close()


def query_data(query_name):
    print("query_data(%s)" % query_name)
    query_array = load_query(query_name)

    query = query_array[0]

    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(query)
    result = c.fetchall()
    conn.commit()
    conn.close()

    dict_results = list()
    for r in result:
        dict_results.append(dict_from_sqlite3_row(r))
    return dict_results

