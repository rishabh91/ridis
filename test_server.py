import socket
import ridis
from threading import Thread

class RidisServer():

  def __init__(self,host='127.0.0.1', port=5005):
    self.rid_obj = ridis.Ridis()
    self.host = host
    self.port = port

  def start_server(self):
    self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server.bind((self.host, self.port))
    self.server.listen(5)
    while 1:
      conn, addr = self.server.accept()
      Thread(target=self.listener, args=([conn])).start()

  def listener(self, conn):
    print("Thread waala call")
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
      conn.send(str.encode(val))

obj = RidisServer()
obj.start_server()
