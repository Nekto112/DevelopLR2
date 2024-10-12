import pandas as pd
import psycopg2


conn = psycopg2.connect(
    dbname="DevelopLR2",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

statuses = "procurementstatuses"
providers = "providers"
procurements = "souvenirprocurements"
ps = "ProcurementSouvenirs"
souvenir = "Souvenirs"
stories = "SouvenirStores"

cur = conn.cursor()

#cur.execute(f"SELECT ID FROM {table} WHERE Name = '{value}'")

cur.execute(f"INSERT INTO {statuses} (Name) VALUES ('cool') RETURNING ID")
statusId = cur.fetchone()

cur.execute(f"INSERT INTO {providers} (Name, Email, ContactPerson) VALUES ('Shop1', 'test@mail.ru', 'Dima') RETURNING ID")
providerId = cur.fetchone()

cur.execute(f"INSERT INTO {procurements} (IdProvider, Data, IdStatus) VALUES ('{providerId[0]}', '2023-02-05', '{statusId[0]}') RETURNING ID")
procurementsId = cur.fetchone()

cur.execute(f"SELECT ID FROM {souvenir} WHERE Id = '68267'")
souvenirId = cur.fetchone()
cur.execute(f"INSERT INTO {ps} (IdSouvenir, IdProcurement, Amount, Price) VALUES ('{souvenirId[0]}', '{procurementsId[0]}', '50', '10') RETURNING ID")
psId = cur.fetchone()

cur.execute(f"INSERT INTO {stories} (IdProcurement, IdSouvenir, Amount) VALUES ('{procurementsId[0]}', '{souvenirId[0]}', '10') RETURNING ID")
storiesId = cur.fetchone()

conn.commit()
conn.close()
