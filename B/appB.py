# Server/App B:
import sys 
import boto3
import tumaemail
import re
import requests # for instance metadata

sts = boto3.client('sts', region_name='us-west-2')
sqs = boto3.client('sqs', region_name='us-east-1')

# Output caller-identity )
# print sts.get_caller_identity();
# using SDK, try to receive 10 messages from SQS;

myq_url = sqs.get_queue_url(QueueName='myq')  

# tumaemail.process("james")
# sys.exit()
def task1():
	while True:
		messages = sqs.receive_message(QueueUrl=myq_url['QueueUrl'],AttributeNames=['All'],MaxNumberOfMessages=1,VisibilityTimeout=10, WaitTimeSeconds=2)
		if 'Messages' in messages: 
			# There are messages
			m_body = messages['Messages'][0]['Body']
			m_handle = messages['Messages'][0]['ReceiptHandle']
			m_timestamp = messages['Messages'][0]['Attributes']['SentTimestamp']
			print m_body
			if "Error" in m_body:
				m_body = m_body.split("=")[1].strip("['\\','\"']")
				print m_body," - ", m_timestamp			
				tumaemail.process("Message body: " + m_body + "\nTimestamp: "+ m_timestamp)
			
			sqs.delete_message(QueueUrl=myq_url['QueueUrl'],ReceiptHandle=m_handle)
		else:
			break


def task2():
	while True:
		messages = sqs.receive_message(QueueUrl=myq_url['QueueUrl'],AttributeNames=['All'],MaxNumberOfMessages=1,VisibilityTimeout=10, WaitTimeSeconds=2)
		if 'Messages' in messages: 
			# There are messages
			m_body = re.sub('[\\\\"]', '', messages['Messages'][0]['Body'])
			m_handle = messages['Messages'][0]['ReceiptHandle']			
			if m_body[-4:]=='.csv':
				m_body = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4').text + \
				': Warning, CSV file found in S3 bucket. Not processed. Image name is: ' + m_body
				tumaemail.process("Message body: " + m_body)
			print m_body  
			sqs.delete_message(QueueUrl=myq_url['QueueUrl'],ReceiptHandle=m_handle)
			
		else: break;

while True:
	task2()
