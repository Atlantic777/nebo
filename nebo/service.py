import os.path

from .aws.EC2Handler import EC2Handler
from .aws.S3Handler import S3Handler


class NeboService:
    def __init__(self, script=None, instance_id=None):
        if script is None and instance_id is None:
            raise ValueError("Either script or instance_id must be provided!")

        if script is not None:
            self._upload_script(script)

        self.instance_id = instance_id
        self.script = script
        self.instance = EC2Handler(InstanceId=self.instance_id)

    def start(self):
        self.instance.new_instance()
        self.instance_id = self.instance.InstanceId
        return self.instance.InstanceId

    def stop(self):
        self.instance.terminate_instance()
        S3Handler().kill_bucket()

    def _upload_script(self, script_filename):
        if not os.path.isfile(script_filename):
            msg = "Script {} does not exist.".format(script_filename)
            raise ValueError(msg)

        S3Handler().ensure(script_filename)
