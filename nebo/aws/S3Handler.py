import boto3
import os.path

DEFAULT_BUCKET = "nhardi-mrkirm2-scripts"
DEFAULT_LOCATION = "eu-central-1"


class S3Handler:
    def __init__(self, bucket=DEFAULT_BUCKET):
        self.bucket = bucket
        self.s3 = boto3.client('s3')

    def ensure(self, filename):
        self._get_or_create_bucket(self.bucket)
        self._upload(filename)

    def kill_bucket(self, bucket=DEFAULT_BUCKET):
        for entry in self.s3.list_objects(Bucket=bucket)['Contents']:
            self.s3.delete_object(Bucket=bucket, Key=entry['Key'])

        self.s3.delete_bucket(Bucket=bucket)
        self.s3.get_waiter('bucket_not_exists').wait(Bucket=bucket)

    def _get_or_create_bucket(self, bucket):
        try:
            self.s3.create_bucket(Bucket=bucket,
                                  CreateBucketConfiguration={
                                      "LocationConstraint": DEFAULT_LOCATION,
                                  })
        except Exception as e:
            pass

    def _upload(self, filename):
        key = os.path.basename(filename)
        self.s3.upload_file(filename, DEFAULT_BUCKET, key)
        self.s3.put_object_acl(Bucket=DEFAULT_BUCKET,
                               Key=key,
                               ACL='public-read',
                               )
