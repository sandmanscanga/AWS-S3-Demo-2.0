"""Module containing the S3 client utilities."""
import argparse
import os
from typing import Dict, Tuple


def get_auth_keys(args: argparse.Namespace,
                  env_access_key_name: str = "S3_ACCESS_KEY",
                  env_secret_key_name: str = "S3_SECRET_KEY"
                  ) -> Tuple[str, str]:
    """Get the access key and secret key."""

    access_key = args.access_key
    if not access_key:
        try:
            access_key = os.environ[env_access_key_name]
        except KeyError:
            access_key = input("Enter the access key: ")

    secret_key = args.secret_key
    if not secret_key:
        try:
            secret_key = os.environ[env_secret_key_name]
        except KeyError:
            secret_key = input("Enter the secret key: ")

    return access_key, secret_key


def get_bucket_info(args: argparse.Namespace,
                    env_bucket_key_name: str = "S3_BUCKET_NAME",
                    env_dir_path_key_name: str = "S3_LOCAL_PATH",
                    env_local_path_key_name: str = "S3_DIR_PATH",
                    env_download_path_key_name: str = "S3_DOWNLOAD_PATH",
                    env_upload_path_key_name: str = "S3_UPLOAD_PATH"
                    ) -> Dict[str, str]:
    """Get the bucket information to download and upload a file."""

    bucket_info_dict = {
        "bucket_name": args.bucket_name or os.environ.get(env_bucket_key_name),
        "local_path": args.local_path or os.environ.get(env_local_path_key_name),
        "dir_path": args.dir_path or os.environ.get(env_dir_path_key_name),
        "download_path": args.download_path or os.environ.get(env_download_path_key_name),
        "upload_path": args.upload_path or os.environ.get(env_upload_path_key_name)
    }

    return bucket_info_dict
