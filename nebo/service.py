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

        self.name = name
        self.instance_id = instance_id
        self.instance = EC2Handler(InstanceId=self.instance_id)

        if self.name is not None:
            self.app_storage = S3Handler(self.name, 'apps')

        if script is not None:
            self.script = script
            self._upload_script(script)
            user_data = self._get_userdata(init,
                                           script_name=script,
                                           service_name=name)
            self.instance.set_userdata(user_data)

        # self.app_storage.ensure(script)
        # url = self.app_storage.get_url(script)

    def start(self):
        self.instance.new_instance()
        self.instance_id = self.instance.InstanceId
        return self.instance.InstanceId

    def stop(self):
        self.instance.terminate_instance()

        if self.name is not None:
            S3Handler(self.name, "apps").kill_bucket()

    def _upload_script(self, script_filename):
        if not os.path.isfile(script_filename):
            msg = "Script {} does not exist.".format(script_filename)
            raise ValueError(msg)

        S3Handler(self.name, "apps").ensure(script_filename)

    def _get_userdata(self, user_provided_init, service_name, script_name):
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
                'SCRIPT_NAME':  os.path.basename(script_name),
                'SERVICE_NAME': service_name,
            }

            return Template(raw_template).render(**context)
