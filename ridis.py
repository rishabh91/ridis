import time


class Ridis():

    def __init__(self):
        self.storage = {}

    def get(self, key):
        if key not in self.storage:
            return "Didnt find the key"
        else:
            current_timestamp = time.time()
            ttl = current_timestamp - self.storage[key][1]
            if ttl > 360:
                del self.storage[key]
                return "The Key Expired"
            else:
                return self.storage[key][0]

    def set(self, key, value):
        if key not in self.storage:
            val = []
            val.append(value)
            val.append(time.time())
            self.storage[key] = val
            return "{} has been set".format(key)
        else:
            current_timestamp = time.time()
            ttl = current_timestamp - self.storage[key][1]
            if ttl > 360:
                del self.storage[key]
                val = []
                val.append(value)
                val.append(time.time())
                self.storage[key] = val
                return "{} has been set".format(key)
            else:
                return "The Key already exists try UPDATE instead"

    def get_all_keys(self):
        return [*self.storage]
