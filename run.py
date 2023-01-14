"""Module containing the functionality to test the AWS S3 client utility."""
import argparse

from client import S3Client
from utils import get_auth_keys


def main(args: argparse.Namespace) -> None:
    """Execute the main process."""

    access_key, secret_key = get_auth_keys(args)

    bucket_name = args.bucket_name
    dir_path = args.dir_path
    local_path = args.local_path
    download_path = args.download_path
    upload_path = args.upload_path

    client = S3Client(access_key, secret_key)

    client.ls(dir_path)
    client.cd(bucket_name, dir_path)

    client.get(bucket_name, download_path, local_path)
    client.put(bucket_name, upload_path, local_path)

    stats = client.stat(bucket_name, download_path)
    is_dir = client.is_dir(bucket_name, dir_path)

    print(f"stats = {stats!r}")
    print(f"is_dir = {is_dir!r}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-a",
                        "--access-key",
                        dest="access_key",
                        help="specify the AWS access key")
    parser.add_argument("-s",
                        "--secret-key",
                        dest="secret_key",
                        help="specify the AWS secret key")
    parser.add_argument("-b",
                        "--bucket-name",
                        dest="bucket_name",
                        help="specify the AWS bucket name")

    parser.add_argument("-d",
                        "--dir-path",
                        dest="dir_path",
                        help="specify the AWS directory path")
    parser.add_argument("-l",
                        "--local-path",
                        dest="local_path",
                        help="specify the AWS local file path")
    parser.add_argument("-g",
                        "--get-path",
                        dest="download_path",
                        help="specify the AWS remote download path")
    parser.add_argument("-p",
                        "--put-path",
                        dest="upload_path",
                        help="specify the AWS remote upload path")

    args = parser.parse_args()

    main(args)
