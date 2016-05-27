import sqlite3

conn = sqlite3.connect("/tmp/animal.db")
# conn.row_factory = sqlite3.Row
cur = conn.cursor()

name = input()

sql = "SELECT * FROM animals WHERE name LIKE ?"
cur.execute(sql, ['%' + name + '%'])
for row in cur:
    print(row)

conn.close()
