import os
import mariadb
from dotenv import load_dotenv

load_dotenv()

connection_dict = {
    "host_set": os.getenv("DB_HOST"),
    "port_set" : os.getenv("DB_PORT"),
    "user_set" : os.getenv("DB_USER"),
    "password_set": os.getenv("DB_PASSWORD"),
    "database_set" : os.getenv("DB_NAME")
}
class Database:
    def __init__(self, host =None, port =None, user=None, password=None, database=None):
        self.host = host or connection_dict["host_set"]
        self.port = int(port or connection_dict["port_set"])
        self.user = user or connection_dict["user_set"]
        self.password = password or connection_dict["password_set"]
        self.database = database or connection_dict["database_set"]

    def get_connection(self):
        return mariadb.connect(host=self.host, port=self.port, user=self.user, password= self.password, database=self.database)
    