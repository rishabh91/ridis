import socket
import ridis
import time
from threading import Thread


class RidisServer():

    def __init__(self, host='127.0.0.1', port=5005):
        self.rid_obj = ridis.Ridis()
        self.host = host
        self.port = port
        Thread(target=self.clear_keys, args=([365])).start()

    def start_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        while 1:
            conn, addr = self.server.accept()
            Thread(target=self.listener, args=([conn])).start()

    def clear_keys(self, time_interval):
        time.sleep(time_interval)
        print("Clear keys called")
        keys = self.rid_obj.get_all_keys()
        for key in keys:
            print(key)
            current_timestamp = time.time()
            ttl = self.rid_obj.storage[key][1]
            if current_timestamp - ttl > 360:
                del self.rid_obj.storage[key]
                print("Removed the key {} from Ridis as it expired".format(key))
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
                key, value = data[1], data[2]
                val = self.rid_obj.set(key, value)
            elif 'KEY *' in data:
                val = self.rid_obj.get_all_keys()
                print(val)
                val = ' '.join(val)
                if len(val) == 0:
                    val = "No Keys Exist"

            conn.send(str.encode(val))


obj = RidisServer()
obj.start_server()
