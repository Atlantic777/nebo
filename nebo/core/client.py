import os
import json
import uuid

from nebo.aws import SQSHandler, S3Handler


class NeboClient:
    def __init__(self, service_name):
        self.service_name = service_name
        self.sqs_requests = SQSHandler(service_name, "input")
        self.input_storage = S3Handler(service_name, "inputs")
        self.output_storage = S3Handler(service_name, "outputs")
        self.sqs_responses = None

    def send_request(self, input_file, args=None):
        self.input_storage.ensure(input_file)

        response_queue_id = uuid.uuid4().hex
        self.sqs_responses = SQSHandler(self.service_name,
                                        response_queue_id)

        input_key = os.path.basename(input_file)
        msg = {
            'input_file_key': input_key,
            'args': args,
            'response_queue': self.sqs_responses.queue_name,
            }

        self.sqs_requests.send_message(json.dumps(msg))

        output_key = None

        resp = self.sqs_responses.get_message()
        self.sqs_responses.delete()

        if resp is not None:
            resp = json.loads(resp)

        if resp is not None and 'key' in resp:
            output_key = resp['key']

        return output_key
