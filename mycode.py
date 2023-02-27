import boto3
import psycopg2
import hashlib
import json
from datetime import datetime

# Connect to the AWS SQS Queue
sqs = boto3.client('sqs', endpoint_url='http://localhost:4566', region_name='us-east-1')
queue_url = 'http://localhost:4566/queue/login-queue'

# Connect to the Postgres database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="postgres"
)
cursor = conn.cursor()

def version_to_int(version: str) -> int:
    version = version.split('.')
    version.reverse()
    version_value = 0
    base = 0
    while len(version) < 3:
        version.append('0')
    for e in version:
        version_value += int(e) * pow(2, base)
        base += 4
    return version_value

while True:

    # Receive messages from queue
    try:
        response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
        if 'Messages' not in response:
            continue
    except Exception as exceptions:
        # Print error while parsing parameters
        print("Error - " + str(exceptions))

        # Exit from program
        sys.exit()

    messages = response['Messages']
    message_count = 0
    for message in messages:
        # Parse the JSON data
        data = json.loads(message['Body'])
        message_count += 1
        try:
            ip = data['ip']
            device_id = data['device_id']
        except Exception as exception:
            # Print message is invalid
            print("Error - Message " + str(message_count) + " is invalid - " + str(exception) + " is not available in queue")

            # Continue to next message
            continue

        print(data)
        # Flatten the data and mask the device_id and ip fields
        user_id = data['user_id']
        device_type = data['device_type']
        masked_ip = hashlib.sha256(ip.encode()).hexdigest()
        masked_device_id = hashlib.sha256(device_id.encode()).hexdigest()
        locale = 'None' if data['locale'] == None else data['locale']
        app_version = version_to_int(data['app_version'])
        create_date = datetime.now().strftime("%Y-%m-%d")

        # Insert the transformed data into the Postgres database
        cursor.execute("INSERT INTO user_logins(user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date) VALUES (%s, %s, %s, %s, %s, %s, %s)", (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date))
        conn.commit()
