def insert_item(cursor, item, insert_statement, values):
    try:
        cursor.execute(insert_statement, values)
    except Exception as e:
        print("\n")
        print(e)
        print(f">>>>>>>>>>>>>>>>>>>>>>>database insert failed for {str(item)}")
        print("\n")


def insert_many(cursor, list, insert_statement, values_list):
    try:
        cursor.executemany(insert_statement, values_list)
    except Exception as e:
        print("\n")
        print(e)
        print(f">>>>>>>>>>>>>>>>>>>>>>>database insert failed for {str(list)}")
        print("\n")


def select_many_records(cursor, query):
    cursor.execute(query)
    for record in cursor.fetchall():
        print(record)
    print("\n")
    print("\n")
