from os import curdir
import mysql.connector
import mysql.connector.cursor


class Cnx:
    _host = "localhost"
    _user = "root"
    _database = ""
    _password = ""
    _port = 3306
    conn: mysql.connector.MySQLConnection = None

    def __init__(
        self, host=_host, user=_user, database=None, password=_password, port=_port
    ):
        """
        Obtem uma estancia a classe MySQLConnection

        Params: host, user, database, password and port

        Return: None
        """
        self._host = host
        self._user = user
        self._nome = database
        self._password = password
        self._port = port

    def connected(self):
        """
        Obtem uma estacia do connector


        Return: con tyoeoff MySQLConnection
        """
        configs = {
            "host": self._host,
            "user": self._user,
            "password": self._password,
            "port": self._port,
            "database": self._nome,
            "charset": "utf8mb4",
        }
        conn = mysql.connector.connect(**configs)

        return conn

    def get_cursor(con: mysql.connector.MySQLConnection):
        """
        Obtem uma estacia do cursor

        Params: con typeoff MySQLConnection

        Return: cursor typeoff MySQLCursor
        """

        return con.cursor()

    def desconected(self):
        """
        Fecha a conexão com o banco de dados

        Return: Bool -> False caso ocorra exceção
        """
        if con != None:
            try:
                con.close()
                return True
            except Exception as e:
                return False
        return True
