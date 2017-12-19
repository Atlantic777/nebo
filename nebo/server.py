import sys
import tempfile
import os
import json
from multiprocessing import Process

from .aws.S3Handler import S3Handler
from .aws.SQSHandler import SQSHandler


class Worker:
    def __init__(self, service_name, script_name):
        self.name = service_name
        self.script_name = script_name

        self.init_storage()
        self.make_workspace()
        self.load_job()
        self.input_queue = SQSHandler(service_name, "input")

    def init_storage(self):
        self.app_storage = S3Handler(self.name, 'apps')
        self.sync_storage = S3Handler(self.name, 'sync')
        self.input_data_storage = S3Handler(self.name, 'inputs')
        self.output_data_storage = S3Handler(self.name, 'outputs')

    def process_one(self):
        msg = self.input_queue.get_message()

        if msg is None:
            print("No messages")
            return

        # key is hash
        dmsg = json.loads(msg)
        key = dmsg['input_file_key']

        # such file is already processed by this service
        if self.output_data_storage.exists(key):
            return

        input_file = os.path.join(self.workspace.name, "input-" + key)
        output_file = os.path.join(self.workspace.name, "output-" + key)

        self.input_data_storage.get(key, input_file)

        task = self.Job(input_file, output_file, msg)
        task.work()

        self.output_data_storage.ensure(output_file, key)
        result_url = self.output_data_storage.url(output_file)
        print("results uploaded")

        if 'response_queue' in dmsg:
            self.notify_client(dmsg['response_queue'], result_url)

        os.remove(input_file)
        os.remove(output_file)

    def make_workspace(self):
        self.workspace = tempfile.TemporaryDirectory(prefix="worker-")

    def load_job(self):
        dst = os.path.join(self.workspace.name, 'job.py')
        self.app_storage.get(self.script_name, dst)

        os.sys.path.append(self.workspace.name)
        import job
        self.Job = job.Job

    def notify_client(self, queue_url, reuslt_url):
        pass


def _worker_thread(service_name, script_name):
    w = Worker(service_name, script_name)

    while True:
        try:
            w.process_one()
        except Exception as e:
            print("The exception handler")
            print(e)


class NeboServer:
    def __init__(self, name, script, workers_count=1):
        self.name = name
        self.script = script

        self.init_input_queue()
        self.init_storage()
        self.spawn_workers(workers_count)

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

    def init_input_queue(self):
        pass

    def init_storage(self):
        pass


def main():
    name = sys.argv[1]
    script = sys.argv[2]

    NeboServer(name, script)


if __name__ == "__main__":
    main()
