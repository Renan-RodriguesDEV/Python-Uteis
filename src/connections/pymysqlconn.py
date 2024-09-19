import pymysql

configs = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "utoopy",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,  # Para retornar resultados como dicionarios
}
# consulta sem parametros
connect = pymysql.connect(**configs)
with connect as cnx:
    with cnx.cursor() as cursor:
        query = "SELECT * FROM emails"
        cursor.execute(
            query,
        )
        result = cursor.fetchall()
        print(f"consulta sem parametros {result}")

# consulta com parametros
connect = pymysql.connect(**configs)
with connect as cnx:
    with cnx.cursor() as cursor:
        query = "SELECT * FROM emails where id = %s"
        cursor.execute(query, 1)
        result = cursor.fetchall()
        print(f"consulta com parametros: {result}")
