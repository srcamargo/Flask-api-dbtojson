import sqlite3
conn = sqlite3.connect("customersdb.db") # ou use :memory: para colocar na memória RAM

cursor = conn.cursor()

# cria uma tabela
cursor.execute("""CREATE TABLE customers
                 (ID text, name text, balance float)
              """)


# insere alguns dados
cursor.execute("INSERT INTO customers VALUES ('1001', 'Juca Jones', '10000')")

# salva dados no banco
conn.commit()
cursor = conn.cursor()
# insere múltiplos registros de uma só vez usando o método "?", que é mais seguro
customers = [('1002', 'John Lennon', '20000'),
         ('1003', 'Paul Mcartney', '30000'),
         ('1004', 'Ringo Star', '40000')]
cursor.executemany("INSERT INTO customers VALUES (?,?,?)", customers)
conn.commit()


# Update
# conn = sqlite3.connect("mydatabase.db")
# cursor = conn.cursor()

# sql = """
# UPDATE albums
# SET artist = 'John Doe'
# WHERE artist = 'Andy Hunter'
# """
# cursor.execute(sql)
# conn.commit()

# Delete
# conn = sqlite3.connect("mydatabase.db")
#cursor = conn.cursor()

# sql = """
# DELETE FROM albums
# WHERE artist = 'John Doe'
# """
# cursor.execute(sql)
# conn.commit()

# Consultas
# import sqlite3

# conn = sqlite3.connect("mydatabase.db")
#conn.row_factory = sqlite3.Row
# cursor = conn.cursor()

# sql = "SELECT * FROM albums WHERE artist=?"
# cursor.execute(sql, [("Red")])
# print cursor.fetchall()  # ou use fetchone()

# print "\nAqui a lista de todos os registros na tabela:\n"
# for row in cursor.execute("SELECT rowid, * FROM albums ORDER BY artist"):
#    print row

# print "\nResultados de uma consulta com LIKE:\n"
# sql = """
# SELECT * FROM albums
# WHERE title LIKE 'The%'"""
# cursor.execute(sql)
# print cursor.fetchall()
