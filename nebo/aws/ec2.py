import boto3

DEFAULT_AMI = "ami-bf2ba8d0"
DEFAULT_TYPE = "t2.micro"
DEFAULT_SECURITY_GROUP = "mrkirm2"
DEFAULT_KEY_NAME = "nhardi_iam_key"
DRY_RUN = False


class EC2Handler:
    def __init__(self, InstanceId=None, AmiId=DEFAULT_AMI,
                 InstanceType=DEFAULT_TYPE):
        self.InstanceId = InstanceId
        self.Description = None
        self.ec2 = boto3.client('ec2')
        self.userdata = ""

    def _ec2_wait(self, State):
        w = self.ec2.get_waiter(State)
        w.wait(InstanceIds=[self.InstanceId])

    def _get_instance_id(self, InstanceObj):
        try:
            instance_id = InstanceObj["Instances"][0]["InstanceId"]
            return instance_id
        except Exception as e:
            print("Something bad happened.")
            return None

    def set_userdata_file(self, filename):
        with open(filename, 'r') as f:
            self.userdata = f.read()

    def set_userdata(self, data):
        self.userdata = data

    def new_instance(self):
        try:
            i = self.ec2.run_instances(ImageId=DEFAULT_AMI, MinCount=1,
                                       MaxCount=1, InstanceType=DEFAULT_TYPE,
                                       SecurityGroups=[DEFAULT_SECURITY_GROUP],
                                       KeyName=DEFAULT_KEY_NAME,
                                       UserData=self.userdata)

            # TODO: check for exceptions
            instance_id = self._get_instance_id(i)
            self.InstanceId = instance_id

            self._ec2_wait("instance_status_ok")

            return i

        except Exception as e:
            print("An error happened in new_instance()")
            print(e)
            return None

    def stop_instance(self):
        try:
            r = self.ec2.stop_instances(InstanceIds=[self.InstanceId])
            self._ec2_wait("instance_stopped")
            return r
        except Exception as e:
            print("An error happened in stop_instance()")
            print(e)
            return None

    def start_instance(self):
        try:
            r = self.ec2.start_instances(InstanceIds=[self.InstanceId])
            self._ec2_wait("instance_running")
            return r
        except Exception as e:
            print("An error happened in start_instance()")
            print(e)
        return None

    def terminate_instance(self):
        try:
            r = self.ec2.terminate_instances(InstanceIds=[self.InstanceId])
            self._ec2_wait("instance_terminated")
            return r
        except Exception as e:
            print("An error happened in terminte_instance()")
            print(e)
            return None

    def describe_instance(self):
        try:
            r = self.ec2.describe_instances(InstanceIds=[self.InstanceId])
            return r["Reservations"][0]["Instances"][0]
        except Exception as e:
            print("An error happened in describe_instance()")
            print(e)
            return None

    def exists(self):
        d = self.describe_instance()

        if d is not None:
            return True
        else:
            return False
