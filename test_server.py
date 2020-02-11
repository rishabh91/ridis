import socket
import ridis
import datetime
import time
import logging
from threading import Thread


class RidisServer():

    def __init__(self, host='127.0.0.1', port=5005):
        self.rid_obj = ridis.Ridis()
        self.host = host
        self.port = port
        Thread(target=self.clear_keys, args=([360])).start()

    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        while 1:
            conn, addr = self.server.accept()
            Thread(target=self.listener, args=([conn])).start()

    def clear_keys(self, time_interval):
        while True:
          time.sleep(time_interval)
          logging.info("Clear keys called")
          keys = self.rid_obj.get_all_keys()
          for key in keys:
            print(key)
            current_timestamp = datetime.datetime.now()
            ttl = self.rid_obj.storage[key][1]
            if current_timestamp > ttl:
              del self.rid_obj.storage[key]
              logging.info("Removed the key {} from Ridis as it expired".format(key))
            else:
              continue

    def listener(self, conn):
        while True:
            val = ''
            data = conn.recv(1024)
            if not data:
                continue
            data = data.decode('utf-8').strip()
            if 'GET' in data:
                key = data.split(' ')[1]
                val = self.rid_obj.get(key)
            elif 'SET' in data:
                data = data.split(' ')
                print(data)
                if len(data) == 4:
                    key, value, ttl = data[1], data[2], data[3]
                    val = self.rid_obj.set(key, value, int(ttl))
                else:
                    key, value = data[1], data[2]
                    val = self.rid_obj.set(key, value)

            elif 'KEY *' in data:
                val = self.rid_obj.get_all_keys()
                print(val)
                val = ' '.join(val)
                if len(val) == 0:
                    val = "No Keys Exist"

            conn.send(str.encode(val))

if __name__ == '__main__':
    RidisServer().start_server()
