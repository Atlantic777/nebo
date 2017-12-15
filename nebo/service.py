from .aws.EC2Handler import EC2Handler


class NeboService:
    def __init__(self, script=None, instance_id=None):
        if script is None and instance_id is None:
            raise ValueError("Either script or instance_id must be provided!")

        self.instance_id = instance_id
        self.script = script
        self.instance = EC2Handler(InstanceId=self.instance_id)

    def start(self):
        self.instance.new_instance()
        self.instance_id = self.instance.InstanceId
        return self.instance.InstanceId

    def terminate(self):
        self.instance.terminate_instance()
