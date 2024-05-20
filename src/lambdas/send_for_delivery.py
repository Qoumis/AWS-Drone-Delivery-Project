import json
import logging
import requests

# Enable logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

provider_endpoint = 'http://ec2-34-228-41-139.compute-1.amazonaws.com:5000/'
headers = {"Content-Type": "application/json"}

def lambda_handler(event, context):
    
    logger.info(event)
    
    #just send the winners (a json with their bids, distance etc) to drone provider ec2
    try:
        # Send the POST request
        response = requests.post(provider_endpoint, data = json.dumps(event), headers = headers)

        logger.info(f"Status Code: {response.status_code}")
        logger.info(response.text)

        return {
            'statusCode': response.status_code,
            'body': response.text
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
