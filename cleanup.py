import boto3
import time

awsProfileName = "put your profile name here"
search = "you should change me"

session = boto3.Session(profile_name=awsProfileName)
s3 = session.client('s3')

response = s3.list_buckets()
bucketList = [bucket for bucket in response['Buckets'] if search in bucket['Name'] ]

print(f'** WARNING, This will delete all buckets with name containing: { search } - { len(bucketList)} buckets found')
time.sleep(5)

for bucket in bucketList:
    print(f'Deleting bucket: {bucket["Name"]} in 3s')
    bucketName = bucket["Name"]
    time.sleep(3)
    for key in s3.list_objects(Bucket=bucketName)['Contents']:
        print("File : ", key['Key'])
        filename = key['Key']
        paginator = s3.get_paginator('list_object_versions')
        response_iterator = paginator.paginate(Bucket=bucketName)
        for response in response_iterator:
            versions = response.get('Versions', [])
            versions.extend(response.get('DeleteMarkers', []))
            for version_id in [x['VersionId'] for x in versions if x['Key'] == filename and x['VersionId'] != 'null']:
                print('Deleting {} version {}'.format(filename, version_id))
                s3.delete_object(Bucket=bucketName, Key=filename, VersionId=version_id)
        s3.delete_object(Bucket=bucketName, Key=filename)

    # Removes the bucket
    s3.delete_bucket(Bucket=bucketName);

print("Done")
