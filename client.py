"""Module containing the AWS S3 client utility."""
import boto3


class S3Client:
    """AWS S3 client wrapper utility."""

    def __init__(self,
                 access_key: str,
                 secret_key: str,
                 bucket: str = "",
                 prefix: str = ""
                 ) -> None:
        """
        Initialize S3 client object.

        :param access_key: AWS access key
        :param secret_key: AWS secret key
        :param bucket: AWS bucket name (optional)
        :param prefix: AWS bucket directory path (optional)
        """

        self.bucket = bucket
        self.prefix = prefix

        self.s3 = boto3.client("s3",
                               aws_access_key_id=access_key,
                               aws_secret_access_key=secret_key)

    def get(self, bucket: str, key: str, local_path: str) -> None:
        """
        Download a file from S3.

        :param bucket: S3 bucket name
        :param key: S3 key (file path and name)
        :param local_path: local file path to save the file
        """

        self.s3.download_file(bucket, key, local_path)

    def put(self, bucket: str, key: str, local_path: str) -> None:
        """
        Upload a file to S3.

        :param bucket: S3 bucket name
        :param key: S3 key (file path and name)
        :param local_path: local file path
        """

        self.s3.upload_file(local_path, bucket, key)

    def cd(self, bucket: str, prefix: str) -> None:
        """
        Set the current "directory" in S3.

        :param bucket: S3 bucket name
        :param prefix: S3 prefix (directory path)
        """

        self.bucket = bucket
        self.prefix = prefix

    def mkdir(self, bucket: str, prefix: str) -> None:
        """
        Create an "empty" directory in S3.

        :param bucket: S3 bucket name
        :param prefix: S3 prefix (directory path)
        """

        self.s3.put_object(Bucket=bucket, Key=prefix)

    def is_dir(self, bucket: str, prefix: str) -> bool:
        """
        Check if a "directory" exists in S3.

        :param bucket: S3 bucket name
        :param prefix: S3 prefix (directory path)
        :return: True if the prefix exists, False otherwise
        """

        is_dir_flag = None

        try:
            self.s3.list_objects(Bucket=bucket, Prefix=prefix)
        except:
            is_dir_flag = False
        else:
            is_dir_flag = True

        return is_dir_flag

    def stat(self, bucket: str, key: str) -> dict:
        """
        Get metadata of a file in S3.

        :param bucket: S3 bucket name
        :param key: S3 key (file path and name)
        :return: a dict containing the file"s size, ETag, LastModified
        """

        obj = self.s3.head_object(Bucket=bucket, Key=key)

        stat_dict = {
            "size": obj["ContentLength"],
            "ETag": obj["ETag"],
            "LastModified": obj["LastModified"]
        }

        return stat_dict

    def ls(self, prefix: str = None) -> list:
        """
        List the contents of a "directory" in S3.

        :param prefix: S3 prefix (directory path)
        :return: a list of the keys(file and directory names) in the specified prefix
        """

        if prefix is None:
            prefix = self.prefix

        result = self.s3.list_objects(Bucket=self.bucket, Prefix=prefix)
        
        contents = []
        for content in result.get("Contents", []):
            contents.append(content.get("Key"))

        return contents
