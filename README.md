# s3-cleanup
Delete S3 Buckets, including all their versioned objects

Buckets will be matched when their name contaied the substring in search.

## Configuration:
* **awsProfileName**: name of you AWS profile (as configured in .aws/credentials)
* **search**: substring for matching bucket names
