import boto3
import requests
import random

sts_client = boto3.client('sts', region_name='us-west-2')

## Assume role
assumedRoleObject = sts_client.assume_role( RoleArn="arn:aws:iam::457629803563:role/app_a_role_a", RoleSessionName="session1" )

ACCESS_KEY = assumedRoleObject['Credentials']['AccessKeyId']; 
SECRET_KEY = assumedRoleObject['Credentials']['SecretAccessKey'];
SESSION_TOKEN = assumedRoleObject['Credentials']['SessionToken'];

session = boto3.Session(aws_access_key_id=ACCESS_KEY,aws_secret_access_key=SECRET_KEY,aws_session_token=SESSION_TOKEN)

# print 'session information\n', session;
# sqs = boto3.client('sqs', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY, aws_session_token=SESSION_TOKEN, region_name='us-east-1');

# create a SQS client using the new session.
sqs = session.client('sqs')

# use list_queues to describe the queues available
# print sqs.list_queues();

# use API Gateway 
headers = {u'content-type': u'application/json'}
url = 'https://0qslx9bdr8.execute-api.us-west-2.amazonaws.com/prod/message';
		
def task1():
	""" Using for..loop """
	for i in range(25):
		if i==3:
			params = {'Error':'Color'}
		elif i==17:
			params = {'Error':'Size'}
		else:
			params = {'x': (random.randrange(0, 101, 2))};		
		
		r = requests.post(url, data=params, headers=headers);
		print(r.status_code, r.reason);		
		
def task2():
	""" using S3 bucket """	
	s3 = session.client('s3')
	bucket_name = 'naburu-ami-buckets'; prefix_name = 'empty';
	# bucket = s3.list_objects_v2(Bucket='naburu-ami-bucketsS',Prefix='many-files',StartAfter='',MaxKeys=1)
	
	kwargs = {'Bucket': bucket_name, 'Prefix' : prefix_name, 'MaxKeys' : 1}

	files = []
	while True:
		bucket = s3.list_objects_v2(**kwargs)
		try:
			b_keys = [{b['Key'].rpartition('/')[0]:b['Key'].rpartition('/')[2]} for b in bucket['Contents'] if len(b['Key'].rpartition('/')[2])>0 ]
			files = files + b_keys
			kwargs['ContinuationToken'] = bucket['NextContinuationToken']
		except KeyError:
			 break

	for f in files:
		f_name = bucket_name + '/' + f.keys()[0] + '/' + f.values()[0]
		r = requests.post(url, data=f_name, headers=headers);
		print f_name
		print(r.status_code, r.reason);


while True:
	task2()
