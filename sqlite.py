import sqlite3

# Nome do arquivo do banco
db_name = "rpg.db"

# Nome do script SQL
sql_file = "sql.sql"   # <- aqui o arquivo que você disse que se chama "sql"

# Conectar ao SQLite (cria o banco se não existir)
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

# Ler o script .sql
with open(sql_file, "r", encoding="utf-8") as f:
    sql_script = f.read()

# Executar o script SQL no banco
cursor.executescript(sql_script)

conn.commit()
conn.close()

print("Banco de dados criado e populado com sucesso!")
