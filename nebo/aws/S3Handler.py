import boto3
import os.path

DEFAULT_BUCKET_PREFIX = "nhardi-mrkirm2-"
DEFAULT_LOCATION = "eu-central-1"


class S3Handler:
    def __init__(self, bucket, directory=None):
        self.bucket = DEFAULT_BUCKET_PREFIX + bucket
        self.prefix = directory
        self.s3 = boto3.client('s3')

    def _make_key(self, filename):
        key = os.path.basename(filename)

        if self.prefix is not None:
            key = self.prefix + "/" + key

        return key

    def ensure(self, filename, key=None):
        if key is None:
            key = filename

        self._get_or_create_bucket(self.bucket)
        self._upload(filename, key)

    def get(self, src, dst):
        # name of the file in bucket
        key = self._make_key(src)
        self.s3.download_file(Bucket=self.bucket, Key=key, Filename=dst)

    def kill_bucket(self, bucket):
        try:
            for entry in self.s3.list_objects(Bucket=bucket)['Contents']:
                self.s3.delete_object(Bucket=bucket, Key=entry['Key'])

            self.s3.delete_bucket(Bucket=bucket)
            self.s3.get_waiter('bucket_not_exists').wait(Bucket=bucket)
        except Exception as e:
            print(e)

    def _get_or_create_bucket(self, bucket):
        try:
            self.s3.create_bucket(Bucket=bucket,
                                  CreateBucketConfiguration={
                                      "LocationConstraint": DEFAULT_LOCATION,
                                  })
        except Exception as e:
            pass

    def _upload(self, filename, key):
        _key = ""

        if key is None:
            _key = self._make_key(filename)
        else:
            _key = self._make_key(key)

        self.s3.upload_file(filename, self.bucket, _key)
        self.s3.put_object_acl(Bucket=self.bucket,
                               Key=_key,
                               ACL='public-read',
                               )

    def exists(self, filename):
        return False

    def wait_for(self, key):
        pass

    def url(self, key):
        pass
