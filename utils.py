"""Module containing the S3 client utilities."""
import argparse
import os


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
