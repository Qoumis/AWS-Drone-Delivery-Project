import json
import boto3
import logging

# Enable logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

DB = boto3.client('dynamodb')
sqs = boto3.client('sqs')
sqs_queue_url = 'https://sqs.us-east-1.amazonaws.com/593367212756/BidQueue'
lambda2 = boto3.client('lambda')

def lambda_handler(event, context):
    data = {
    "drones": "",
    "clients": []
    }
    # Get number of available drones
    drones = 0
    paginator = DB.get_paginator('scan')
    for page in paginator.paginate(TableName='Drones'):
        for item in page.get('Items', []):
            if item.get('isAvailable'):
                drones += 1
    logger.info(f"Number of available drones: {drones}")
    data["drones"] = drones
    
    # Get all requests from SQS
    requests = 0
    while True:
        sqs_response = sqs.receive_message(
            QueueUrl=sqs_queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=10,
            WaitTimeSeconds=5
        )
        
        logger.info(f"Received {len(sqs_response.get('Messages', []))} messages from SQS")
        #Stop when queue is empty
        if(len(sqs_response.get('Messages', [])) == 0):
            break
        
        
        for message in sqs_response.get('Messages', []):
            logger.info(f"Received Message: {message['Body']}")
            requests+= 1
            data["clients"].append(json.loads(message['Body']))
            logger.info(data["clients"])
            
            # Delete the message from the queue
            sqs.delete_message(
                QueueUrl=sqs_queue_url,
                ReceiptHandle=message['ReceiptHandle']
            )
    
    #forward it to second lambda
    resp = lambda2.invoke(
            FunctionName = 'find_optimal_requests',
            InvocationType = 'RequestResponse',
            Payload = json.dumps(data,indent=2)
    )
    
    logger.info('--------------')
    logger.info(resp['Payload'].read().decode('utf-8'))
    
    return {
        'statusCode': 200,
        'body': json.dumps(f'{requests} requests have been forwarded to lambda2')
    }
