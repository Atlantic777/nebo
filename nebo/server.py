import sys

from multiprocessing import Process
from .aws.S3Handler import S3Handler


class Worker:
    def __init__(self, service_name, script_name):
        self.init_storage()
        # self.input_queue = SQSHandler(service_name)
        # make workspace
        # get Job script

    def init_storage(self):
        self.app_storage = S3Handler(self.name, 'apps')
        self.input_data_storage = S3Handler(self.name, 'inputs')
        self.output_data_storage = S3Handler(self.name, 'outputs')

    def process_one(self):
        # msg = self.input_queue.get_message()
        # check if already processing
        # prepare input
        # prepare output
        # task = self.Job(input, output)
        # task.work()
        # upload output
        pass

    def make_workspace(self):
        pass

    def get_job_script(self):
        pass


def _worker_thread(worker):
    w = Worker()

    while True:
        try:
            w.process_one()
        except Exception as e:
            print(e)


class NeboServer:
    def __init__(self, name, script):
        self.name = name
        self.script = script

        self.init_input_queue()
        self.init_storage()
        self.spawn_workers(2)

    def spawn_workers(self, count=1):
        self.workers = []

        for i in range(count):
            w = Process(target=_worker_thread, args=(self.name, self.script))
            self.workers.append(w)

        for p in self.workers:
            p.start()

        for p in self.workers:
            p.join()

    def create_input_queue(self):
        pass


if __name__ == "__main__":
    name = sys.argv[1]
    script = sys.argv[2]

    NeboServer(name, script)
