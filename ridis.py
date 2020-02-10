import datetime
import config

class Ridis():

    def __init__(self):
        self.storage = {}

    def get(self, key):
        if key not in self.storage:
            return "Didnt find the key"
        else:
            current_timestamp = datetime.datetime.now()
            ttl = self.storage[key][1]
            if current_timestamp >= ttl:
                del self.storage[key]
                return "The Key Expired"
            else:
                return self.storage[key][0]

    def set(self, key, value, ttl=config.TTL):
        if key not in self.storage:
            val = []
            val.append(value)
            current_time = datetime.datetime.now()
            ttl = datetime.timedelta(seconds=ttl)
            val.append(current_time + ttl)
            self.storage[key] = val
            return "{} has been set".format(key)
        else:
            current_timestamp = datetime.datetime.now()
            ttl = self.storage[key][1]
            if current_timestamp >= ttl:
                del self.storage[key]
                val = []
                val.append(value)
                val.append(current_timestamp + datetime.timedelta(seconds=ttl))
                self.storage[key] = val
                return "{} has been set".format(key)
            else:
                return "The Key already exists try UPDATE instead"

    def get_all_keys(self):
        return [*self.storage]


