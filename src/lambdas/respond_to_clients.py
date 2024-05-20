import json
import logging
import boto3

sns_client = boto3.client('sns')

# Enable logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    data = {}
    
    logger.info(event)
    for w in event['winners']:
        data[w['id']] = 'delivered'
    
    for l in event['losers']:
        data[l['id']] = 'declined'
    
    response = sns_client.publish(
        TopicArn = 'arn:aws:sns:us-east-1:593367212756:ClientSNS',
        Message = json.dumps(data)
    )
    
    return event

