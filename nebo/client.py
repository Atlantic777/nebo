import os
import json

from .aws.SQSHandler import SQSHandler
from .aws.S3Handler import S3Handler


class NeboClient:
    def __init__(self, service_name):
        self.sqs_requests = SQSHandler(service_name, "input")
        self.input_storage = S3Handler(service_name, "inputs")
        self.output_storage = S3Handler(service_name, "outputs")
        self.sqs_responses = None

    def send_request(self, input_file, args=None):
        self.input_storage.ensure(input_file)

        # key should be hash
        input_key = os.path.basename(input_file)
        msg = {
            'input_file_key': input_key,
            'args': args,
            }

        if self.sqs_responses is not None:
            msg['response_queue'] = self.sqs_responses.url

        resp = self.sqs_requests.send_message(json.dumps(msg))

        output_key = None

        if self.sqs_responses is None:
            output_key = input_key
            self.output_storage.wait_for(output_key)
        else:
            resp = self.sqs_responses.get_message()
            output_key = resp['key']

        return self.output_storage.url(output_key)
