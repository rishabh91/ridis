import time

class Ridis():

	def __init__(self):
		self.__storage = {}

	def get(self, key):
		if key not in self.__storage:
			return "Didnt find the key"
		else:
			current_timestamp = time.time()
			ttl =  current_timestamp - self.__storage[key][1]
			if ttl > 360:
				del self.__storage[key]
				return "The Key Expired"
			else:
				return self.__storage[key][0]

	def set(self, key, value):
		if key not in self.__storage:
			val = []
			val.append(value)
			val.append(time.time())
			self.__storage[key] = val
			return "{} has been set".format(key)
		else:
			current_timestamp = time.time()
			ttl = current_timestamp - self.__storage[key][1]
			if ttl > 360:
				del self.__storage[key]
				val = []
				val.append(value)
				val.append(time.time())
				self.__storage[key] = val
				return "{} has been set".format(key)
			else:
				return "The Key already exists try UPDATE instead"
