import mysql.connector

class MySQLDatabase:
    def __init__(self, host, user, password, database, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    def get_connection(self):
        return mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        )

    def insert_log(self, log_data):
        """
        将日志数据插入到 MySQL 中。假设数据库中有一张 logs 表，
        表结构：id（自增主键）、timestamp（INT）、level（VARCHAR）、message（TEXT）、category（VARCHAR）
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        query = ("INSERT INTO logs (timestamp, level, message, category) "
                 "VALUES (%s, %s, %s, %s)")
        cursor.execute(query, (
            log_data.get("timestamp"),
            log_data.get("level"),
            log_data.get("message"),
            log_data.get("category")
        ))
        conn.commit()
        cursor.close()
        conn.close()
