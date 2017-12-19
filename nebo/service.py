import os.path

from .aws.EC2Handler import EC2Handler
from .aws.S3Handler import S3Handler
from .data import DEFAULT_INIT_TEMPLATE

import boto3
from jinja2 import Template


class NeboService:
    def __init__(self, script=None, instance_id=None, init=None,
                 name=None):
        if (script is None or name is None) and instance_id is None:
            raise ValueError("Either script or instance_id must be provided!")

        if script is not None:
            self._upload_script(script)

        self.instance_id = instance_id
        self.script = script
        self.instance = EC2Handler(InstanceId=self.instance_id)

        user_data = self._get_userdata(init)
        self.instance.set_userdata(user_data)

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

    def _get_userdata(self, user_provided_init):
        if user_provided_init is not None:
            with open(user_provided_init) as f:
                user_data = ''.join(f.readlines())
                return user_data
        else:
            raw_template = None
            with open(DEFAULT_INIT_TEMPLATE) as f:
                raw_template = f.read()

            s = boto3.Session()
            creds = s.get_credentials()

            context = {
                'ACCESS_KEY': creds.access_key,
                'SECRET_KEY': creds.secret_key,
            }

            return Template(raw_template).render(**context)
