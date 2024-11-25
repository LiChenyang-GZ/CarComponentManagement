import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE mappingTable (num INTEGER PRIMARY KEY, fail_code TEXT, '
            'component TEXT, fail_mode TEXT, component_id TEXT, fail_mode_id TEXT)')
print("Table fail mode created successfully")
conn.execute('CREATE TABLE failModesTable (num INTEGER PRIMARY KEY, name TEXT, describe TEXT)')
print("Table fail mode created successfully")
conn.execute('CREATE TABLE componentTable (num INTEGER PRIMARY KEY, name TEXT, contact TEXT, manufacturer TEXT)')
print("Table component created successfully")
# conn.execute('ALTER TABLE componentTable ADD fail_rate TEXT')
# print("Table component changed successfully")
# conn.execute('CREATE TABLE topFailRateTable (num INTEGER PROMARY KEY, name TEXT)')
# print("Table top fail rate created successfully")
#cur = conn.cursor()
#cur.execute("SELECT name FROM mappingTable GROUP BY component ORDER BY COUNT(component) DESC")
# response = cur.fetchmany(5)
# print(response)
# conn.close()
