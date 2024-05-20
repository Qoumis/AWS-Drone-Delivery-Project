from flask import Flask, request
import requests
import boto3
import sys
import logging
import random
import time
import json

client_id = int(sys.argv[1])
port = 5000 + client_id
log_file_path = f'client_logs/client_{client_id}.txt'
app = Flask(f"Client {client_id}")

#setup logging stuff
formatter = logging.Formatter('Client {} - %(asctime)s: %(message)s'.format(client_id), datefmt='%Y-%m-%d %H:%M:%S')
handler = logging.FileHandler(log_file_path)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

#aws credentials
region = 'us-east-1'
aws_access_key_id='ASIAYUJ3RELKFMSNNC4U'
aws_secret_access_key='DV+z2Nqk0PlGaP76PO3b991Jv0vNUUbjt9hPaujI'
aws_session_token='FwoGZXIvYXdzEKL//////////wEaDARSLv8bdIMRRwSeRiLDAXcV8tYV/jCgWggEd0Upt+eluo8DTwEcwFZrRpBCQL2uPlqSWfEwX9XY/l/6boXViD6MqW8pbiU+D7eR9Wh3iAn0uO8TNYsE4bQ5zmcoQnFYgthEi5LQ1GMZvySoPF/hwxn9iU>
sns_client = boto3.client('sns',
        aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name = region)

sqs_client = boto3.client('sqs',
        aws_access_key_id = aws_access_key_id,
        aws_secret_access_key = aws_secret_access_key,
        aws_session_token=aws_session_token,
        region_name = region)


@app.route('/',methods = ['GET'])
def get_response():
        app.logger.info(f"{time.time() - init_time } seconds have passed")
        return f'{time.time() - init_time} seconds have passed'

@app.route('/', methods=['POST'])
def sns_endpoint():
        if request.json.get('Type') == 'SubscriptionConfirmation':
                # Extract the SubscribeURL from the SNS confirmation message
                subscribe_url = request.json.get('SubscribeURL')
                response = requests.get(subscribe_url)
                app.logger.info('Subscribed to SNS topic')
                print("Confirmation response:")
                print(response.text)
        else:
                data = request.get_data().decode('utf-8')
                print(data)
                message = json.loads(request.json.get('Message'))
                if message.get(str(client_id)) == "delivered":
                        app.logger.info("Exiting : Product delivered (happy)")
                elif message.get(str(client_id)) == "declined":
                        if (time.time() - init_time) > wait_time :
                                app.logger.info("Exiting : waiting time surpassed (sad)")
                        else :
                                app.logger.info("Entering next round")
                                global bid
                                bid = random.randint(5,25)
                                send_request_sqs()
                else:
                        print("Exw teleiwsei koumparo!")

        return 'OK', 200

def init_profile():
        bid = random.randint(5,25)
        wait_time = random.randint(180,420) #wait time in seconds (3-7 mins)
        distance = round(random.uniform(0.5, 50.0), 1)
        init_time = time.time()
        curr_round = 1
        return bid, wait_time, distance, init_time, curr_round

def sns_subscribe():
        response = sns_client.subscribe(
                TopicArn = 'arn:aws:sns:us-east-1:593367212756:ClientSNS',
                Protocol = 'http',
                Endpoint = f'http://ec2-204-236-203-192.compute-1.amazonaws.com:{port}'
        )

def send_request_sqs():
        data = {
                "id": client_id,
                "distance": distance,
                "bid": bid
        }
        response = sqs_client.send_message(
                QueueUrl = 'https://sqs.us-east-1.amazonaws.com/593367212756/BidQueue',
                MessageBody = json.dumps(data)
        )
        global curr_round
        app.logger.info(f'My bid for this round (round {curr_round}) is {bid}')
        curr_round += 1


if __name__ == '__main__':
   #initialize client profile
        bid, wait_time, distance, init_time, curr_round = init_profile()
        app.logger.info(f"Initialized: Distance {distance}km. I'll wait for {wait_time} seconds.")
        sns_subscribe()
        send_request_sqs()
        app.run(host='0.0.0.0', port=port, debug=False)
