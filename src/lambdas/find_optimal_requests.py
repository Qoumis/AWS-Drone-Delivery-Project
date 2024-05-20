import json
import logging
import boto3

# Enable logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

lambda2 = boto3.client('lambda')

def lambda_handler(event, context):
    # TODO implement
     
    logger.info(event)
    
    winners = {"clients" : []} #optimal bids - winning clients
    all_clients  = {"winners" : [], "losers": []} 
    
    if(len(event['clients']) > event['drones']):
        sorted_clients = sorted(event['clients'], key = lambda x: x['bid'], reverse = True)
        winners['clients'] = sorted_clients[:5]
        all_clients['winners']  = sorted_clients[:5]
        all_clients['losers']  = sorted_clients[5:]
    else: #when #requests are less than the #drones (X)
        winners['clients'] = event['clients']
        all_clients['winners']  = event['clients']
        
    logger.info(f"Winners : {winners}")
    logger.info(f"All clients  : {all_clients}")
    
    #forward winning clients (optimal bids) to drone provider
    resp = lambda2.invoke(
        FunctionName = 'send_for_delivery',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(winners,indent=2)
    )
    
    logger.info('-------Winners forwarded-------')
    logger.info(resp['Payload'].read().decode('utf-8'))
    
    #forward all requests to other lambda that will notify clients for the results
    resp = lambda2.invoke(
        FunctionName = 'respond_to_clients',
        InvocationType = 'RequestResponse',
        Payload = json.dumps(all_clients,indent=2)
    )
    logger.info('------all clients forwarded--------')
    logger.info(resp['Payload'].read().decode('utf-8'))
    
    return {
        "winners" : json.dumps(winners),
        "losers": json.dumps(all_clients['losers'])
        
    }

