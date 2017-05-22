import csv, sqlite3

con = sqlite3.connect("nodes_tags.db")
cur = con.cursor()
cur.executescript("""
    DROP TABLE IF EXISTS t;
    CREATE TABLE nodes_tags (id INTEGER, key TEXT, value TEXT, type TEXT);
    """)

with open('../prepare_for_sql/nodes_tags.csv') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['key'], unicode(i['value'],'utf8'), i['type']) for i in dr]

cur.executemany("INSERT INTO nodes_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
con.commit()
con.close
