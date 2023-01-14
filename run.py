"""Module containing the functionality to test the AWS S3 client utility."""
import argparse
import os

from client import S3Client
from utils import get_auth_keys, get_bucket_info


def main(args: argparse.Namespace) -> None:
    """Execute the main process."""

    print("[*] Fetching auth keys and bucket info.")
    access_key, secret_key = get_auth_keys(args)
    bucket_info_dict = get_bucket_info(args)

    print("[*] Creating local directory for downloaded files.")
    if bucket_info_dict["local_path"]:
        os.makedirs(bucket_info_dict["local_path"], exist_ok=True)

    print("[*] Starting the S3 client.")
    client = S3Client(access_key,
                      secret_key,
                      bucket=bucket_info_dict["bucket_name"],
                      prefix=bucket_info_dict["dir_path"])

    print("[*] Executing the 'ls' and 'cd' commands.")
    client.ls(bucket_info_dict["dir_path"])
    client.cd(bucket_info_dict["bucket_name"],
              bucket_info_dict["dir_path"])

    print("[*] Executing 'get' and 'put' operations.")
    client.get(bucket_info_dict["bucket_name"],
               bucket_info_dict["download_path"],
               bucket_info_dict["local_path"])
    client.put(bucket_info_dict["bucket_name"],
               bucket_info_dict["upload_path"],
               bucket_info_dict["local_path"])

    print("[*] Executing 'stat' and 'is_dir' operations.")
    stats = client.stat(bucket_info_dict["bucket_name"],
                        bucket_info_dict["download_path"])
    is_dir = client.is_dir(bucket_info_dict["bucket_name"],
                           bucket_info_dict["dir_path"])

    print("[*] Displaying 'stat' and 'is_dir' results.")
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
