"""Module containing the functionality to test the AWS S3 client utility."""
import argparse
import json
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
        dir_parts = bucket_info_dict["local_path"].split(os.path.sep)[:-1]
        dir_path_folder = os.path.sep.join(dir_parts)
        os.makedirs(dir_path_folder, exist_ok=True)

    print("\n[*] Starting the S3 client.")
    client = S3Client(access_key,
                      secret_key,
                      bucket=bucket_info_dict["bucket_name"],
                      prefix=bucket_info_dict["dir_path"])

    print("\n[*] Executing 'get' and 'put' operations.")
    client.get(bucket_info_dict["bucket_name"],
               bucket_info_dict["download_path"],
               bucket_info_dict["local_path"])
    client.put(bucket_info_dict["bucket_name"],
               bucket_info_dict["upload_path"],
               bucket_info_dict["local_path"])

    print("\n[*] Executing the 'ls' command.")
    results = client.ls(bucket_info_dict["dir_path"])
    print(f"[*] Results from the 'ls' command: {results=}")

    print("\n[*] Executing 'stat' and 'is_dir' operations.")
    for result in results:
        found_path = os.path.sep.join((bucket_info_dict["dir_path"], result))

        print(f"\n[*] Trying: {found_path}.")
        is_dir = client.is_dir(bucket_info_dict["bucket_name"], found_path)
        if not is_dir:
            stats = client.stat(bucket_info_dict["bucket_name"], found_path)
            # print(f"[+] Results from the 'stat' command: {json.dumps(stats, indent=4)}")
            print(f"[+] Results from the 'stat' command: {json.dumps(stats, indent=4)}")
        else:
            print(f"[-] The result, {result!r}, is a directory.")



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
