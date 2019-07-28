import datetime


class Task:

    def __init__(self, _id):
        self.id = _id
        self.create_time = datetime.datetime.now()
        self.start_time = None
        self.time_to_execute = None
        self.status = "In Queue"

    def run(self):
        self.start_time = datetime.datetime.now()
        self.status = "Run"

    def complete(self):
        self.status = "Completed"
        self.time_to_execute = str(datetime.datetime.now() - self.start_time)

    def __repr__(self):
        return str({"create_time": str(self.create_time),
                    "start_time": str(self.start_time),
                    "status": self.status,
                    "time_to_execute": self.time_to_execute})
