import sqlite3

conn = sqlite3.connect("db.sqlite3")
cur = conn.cursor()
updates = [
    "UPDATE core_aviso SET visualizacao = '[]' WHERE visualizacao IS NULL OR TRIM(visualizacao) = ''",
    "UPDATE core_quadroaviso SET visualizacao = '[]' WHERE visualizacao IS NULL OR TRIM(visualizacao) = ''",
    "UPDATE core_comunicado SET visualizacao = '[]' WHERE visualizacao IS NULL OR TRIM(visualizacao) = ''",
    "UPDATE core_aviso SET visualizacao = json_array(visualizacao) WHERE json_valid(visualizacao) = 0",
    "UPDATE core_quadroaviso SET visualizacao = json_array(visualizacao) WHERE json_valid(visualizacao) = 0",
    "UPDATE core_comunicado SET visualizacao = json_array(visualizacao) WHERE json_valid(visualizacao) = 0",
]
for sql in updates:
    cur.execute(sql)

conn.commit()
conn.close()
print("OK")
