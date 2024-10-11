import csv
import psycopg2

conn = psycopg2.connect(
    dbname="DevelopLR2",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()


def insert_data(table_name, columns, data):
    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(columns))})"
    cursor.execute(query, data)


with open('categories.txt', encoding='utf-8') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        row[1] = row[1] if row[1] else None
        insert_data('SouvenirCategories', ['ID', 'IdParent', 'Name'], row)


conn.commit()
cursor.close()
conn.close()
