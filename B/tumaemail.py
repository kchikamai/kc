import boto3
from botocore.exceptions import ClientError

ses = boto3.client('ses',region_name='us-east-1')

SENDER = "Naburu Mmasaba ruma <letingdarel@gmail.com>"
RECIPIENT = "letingdarel@gmail.com" #  "letingdarel@gmail.com" administrator@kchikama.myinstance.com
CONFIGURATION_SET = "jarib"
AWS_REGION = "us-east-1"
CHARSET = "UTF-8"
SUBJECT = "projo 1"
html_mode = True # True False


def process(message):	
	tuma(create_message(message))
	print 'Sawaz'
	
	
def create_message(message):
	format = 'Text'
	if html_mode:
		message = \
		"""<html>
			<head></head>
			<body>
				<h1>Error</h1>
				<p> """ + str(message) + """ </p>
				<p>
					This email was sent with <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the <a href='https://aws.amazon.com/sdk-for-python/'> AWS SDK for Python (Boto) </a>.
				</p>
			</body>
		</html> """  
		format = 'Html' 
	return {format:message}
	
	
def tuma(body):
	try:
		#Provide the contents of the email.
		response = ses.send_email(
			Destination={'ToAddresses': [RECIPIENT,],},
			Message={
				'Body': {
					# 'Html': {'Charset': CHARSET, 'Data': BODY_HTML,},
					# 'Text': {'Charset': CHARSET, 'Data': ('BODY_TEXT'),},
					body.keys()[0]: {'Charset': CHARSET, 'Data': body.values()[0],},
				},
				'Subject': {'Charset': CHARSET, 'Data': SUBJECT,},
			},
			Source=SENDER, 
			ConfigurationSetName=CONFIGURATION_SET,
		)
	# Display an error if something goes wrong.	
	except ClientError as e:
		print(e.response['Error']['Message'])
	else:
		print("Email sent! Message ID:"),
		print(response['MessageId'])
