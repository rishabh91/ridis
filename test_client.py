import socket
import logging

class RidisClient():

    def __init__(self, host='127.0.0.1', port=5005):
        self.host = host
        self.port = port
        self.client_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_conn.connect((self.host, self.port))

    def client_set(self, query_str=''):
        logging.info("The Query String is {}".format(query_str))
        v = self.client_conn.send(str.encode(query_str))
        response = self.client_conn.recv(1024)
        logging.info(repr(response))


    def client_get(self, query_string):
        logging.info("The Query String is {}".format(query_string))
        self.client_conn.send(str.encode(query_string))
        response = self.client_conn.recv(1024)
        logging.info(repr(response))

if __name__ == '__main__':
    client = RidisClient()
    client.client_set("SET a 12 30")
    client.client_set("SET b 13 10")
    client.client_set("SET c 14 10")
    client.client_get("GET a")
    client.client_get("GET b")
    client.client_get("KEY *")
    client.client_set("SET a 15")
