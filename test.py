from datetime import datetime
import json
from datetime import datetime


class My_json():
    def __init__(self):
        self.datetime = str()
        self.command = str()

    def __str__(self):
        return str(self.datetime) + "\t\t" + str(self.command)

    def append(self, json_file, str_to_append):
        with open(logfile, 'w') as f:
            json.dump(str_to_append, indent=4)  # сериализация JSON
#            f.write(json.dumps(my_json))
        f.close()


my_json = My_json()
logfile = "diploma_log.json"

str_to_append = dict()

now = datetime.now() # current date and time
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
#print("date and time:",date_time)

command = "lowprice"

str_to_append = {'08/07/2022, 17:44:03': 'highprice'}


print(str_to_append)

with open(logfile, 'a') as f:
    json.dump(str_to_append, f, indent=4)  # сериализация JSON

f.close()
