# AWS-S3-Demo-2.0

This is an example client utilizing the AWS S3 software and the Python *boto3* library.

---

## Setting Up AWS S3 Bucket

After configuring an example AWS S3 bucket, the directory structure should match the following:

```
<your-bucket-name>
└── testing/
    ├── download/
    │   └── example.txt
    └── upload/
```

The example.txt file, which is a very simple file, can be found in the `sample-files` directory.

---

## Install & Execute Instructions

To execute the testing script, run the following commands:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
python run.py
```
