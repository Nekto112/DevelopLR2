import pandas as pd
import psycopg2


conn = psycopg2.connect(
    dbname="DevelopLR2",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)


df = pd.read_excel('data.xlsx')

colors = {}
materials = {}
application_methods = {}
categories = {}


def add_value_to_dict_and_db(conn, table, value, dict_name):
    cur = conn.cursor()
    cur.execute(f"SELECT ID FROM {table} WHERE Name = '{value}'")
    row = cur.fetchone()
    if row is None:
        cur.execute(f"INSERT INTO {table} (Name) VALUES ('{value}') RETURNING ID")
        row = cur.fetchone()
        dict_name[value] = row[0]
    else:
        dict_name[value] = row[0]
    return dict_name[value]


for index, row in df.iterrows():
    colors[row['color']] = add_value_to_dict_and_db(conn, 'Colors', row['color'], colors)
    materials[row['material']] = add_value_to_dict_and_db(conn, 'SouvenirMaterials', row['material'], materials)
    application_methods[row['applicMetod']] = add_value_to_dict_and_db(conn, 'ApplicationMethods', row['applicMetod'], application_methods)


cur = conn.cursor()
for index, row in df.iterrows():
    try:
        cur.execute("""
            INSERT INTO Souvenirs (
                ShortName,
                Name,
                Description,
                Rating,
                IdCategory,
                IdColor,
                Size,
                IdMaterial,
                Weight,
                QTopics,
                PicsSize,
                IdApplicMethod,
                AllCategories,
                DealerPrice,
                Price
            ) VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            ) RETURNING ID
        """, (
            row['shortname'],
            row['name'],
            row['description'],
            row['rating'],
            int(row['categoryid']),
            colors[row['color']],
            row['prodsize'],
            materials[row['material']],
            float(row['weight']) if pd.notna(row['weight']) else None,
            float(row['qtypics']) if pd.notna(row['qtypics']) else None,
            row['picssize'],
            application_methods[row['applicMetod']],
            False,
            float(row['dealerPrice']) if pd.notna(row['dealerPrice']) else None,
            float(row['price']) if pd.notna(row['price']) else None
        ))
    except psycopg2.errors.NumericValueOutOfRange as e:
        print(f"Ошибка NumericValueOutOfRange: {e}")
        print(f"Столбцы: {row}")
        print(
            f"Значения: {[float(x) if pd.notna(x) else None for x in [row['weight'], row['qtypics'], row['dealerPrice'], row['price']]]}")


conn.commit()
conn.close()
