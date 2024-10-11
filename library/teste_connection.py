import pyodbc

# Configurações da conexão
server = 'bbz.mine.nu:1433'
port = 1433  # Porta de conexão
database = 'SIGADM'
username = 'AppConnectPay'
password = 'a@s67t2h3n@#BB$Z'

# Define a string de conexão
conn_str = "DRIVER={ODBC Driver 17 for SQL Server};SERVER=bbz.mine.nu:1433;DATABASE=SIGADM;UID=AppConnectPay;PWD=a@s67t2h3n@#BB$Z;Timeout=30"

# Estabelece a conexão
conn = pyodbc.connect(conn_str)

# Cria um cursor
cursor = conn.cursor()

# Executa uma consulta
cursor.execute("SELECT * FROM cndcondo")

# Obtém os resultados
results = cursor.fetchall()

# Imprime os resultados
for row in results:
    print(row)

# Fecha o cursor e a conexão
cursor.close()
conn.close()