"""Module containing the AWS S3 client utility."""
import os

import boto3
import botocore


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

    def is_dir(self, bucket: str, key: str) -> bool:
        """
        Check if a "directory" exists in S3.

        :param bucket: S3 bucket name
        :param prefix: S3 prefix (directory path)
        :return: True if the prefix exists, False otherwise
        """

        is_dir_flag = None

        try:
            self.s3.head_object(Bucket=bucket, Key=key)
        except botocore.exceptions.ClientError:
            is_dir_flag = True
        else:
            is_dir_flag = False

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
            "timestamp": str(obj["LastModified"])
            # "timestamp": int(obj["LastModified"].timestamp())
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

        results = self.s3.list_objects(Bucket=self.bucket, Prefix=prefix)
        
        _contents = set()
        for result in results.get("Contents", []):
            _content = result.get("Key")
            if not _content.rstrip("/") == prefix.rstrip("/"):
                content = _content.split(os.path.sep)[1]
                _contents.add(content)

        return sorted(_contents)
