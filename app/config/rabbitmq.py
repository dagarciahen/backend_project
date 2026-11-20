import os
import pika
from dotenv import load_dotenv

load_dotenv()

connection_dict = {
    "host_set": os.getenv("RABBITMQ_HOST"),
    "port_set" : os.getenv("RABBITMQ_PORT"),
    "user_set" : os.getenv("RABBITMQ_USER"),
    "password_set": os.getenv("RABBITMQ_PASSWORD"),
}
class RabbitMQ:
    def __init__(self, host =None, port =None, user=None, password=None):
        self.host = host or connection_dict["host_set"]
        self.port = int(port or connection_dict["port_set"])
        self.user = user or connection_dict["user_set"]
        self.password = password or connection_dict["password_set"]
        self.connection = None

    def get_connection(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        parameters = pika.ConnectionParameters(host = self.host, port = self.port, credentials=credentials)
        self.connection = pika.BlockingConnection(parameters)
        return self.connection

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()


    