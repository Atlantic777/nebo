import boto3

DEFAULT_QUEUE_PREFIX = "nhardi-mrkirm2-"
TIMEOUT = 10


class SQSHandler:
    def __init__(self, service_name, queue_name):
        self.service_name = service_name
        self.queue_name = queue_name

        self.full_name = self._make_name()

        self.client = boto3.client('sqs')
        resp = self.client.create_queue(QueueName=self.full_name)

        self.url = resp['QueueUrl']

    def get_message(self):
        resp = self.client.receive_message(QueueUrl=self.url,
                                           WaitTimeSeconds=TIMEOUT)

        if 'Messages' not in resp:
            return None

        msg = resp['Messages'][0]
        body = msg['Body']
        handle = msg['ReceiptHandle']

        self.client.delete_message(QueueUrl=self.url, ReceiptHandle=handle)

        return body

    def send_message(self, msg):
        return self.client.send_message(QueueUrl=self.url, MessageBody=msg)

    def get_url(self):
        self.client.get_queue_url(QueueName=self.full_name)['QueueUrl']

    def _make_name(self):
        name = "-".join([
            DEFAULT_QUEUE_PREFIX,
            self.service_name,
            self.queue_name,
        ])
        return name

    def delete(self):
        self.client.delete_queue(QueueUrl=self.url)
