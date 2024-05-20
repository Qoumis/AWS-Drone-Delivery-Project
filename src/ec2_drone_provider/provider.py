from flask import Flask, request
import logging
import json

log_file_path = 'provider_logs.txt'
app = Flask(f"Drone Provider")

#setup logging stuff
formatter = logging.Formatter('Update - %(asctime)s: %(message)s'.format(), datefmt='%Y-%m-%d %H:%M:%S')
handler = logging.FileHandler(log_file_path)
handler.setFormatter(formatter)
app.logger.addHandler(handler)
app.logger.setLevel(logging.INFO)

round_cnt = 1
distance_weight = 0.85
bid_weight = 0.15

def deliver_products(clients):

    #calculate the provider's utility for each client
    for client in clients:
        client['utility'] = round(distance_weight * (10 / client['distance']) + bid_weight * client['bid'], 2)
        print(client)
    ordered_clients = sorted(clients, key = lambda x: x['utility'], reverse = True)
    print(ordered_clients)

    global round_cnt
    app.logger.info(f'*** Schedule in order for round {round_cnt} ***:')
    for client in ordered_clients:
        app.logger.info(f"Client {client['id']} with distance: {client['distance']}km, Bid: {client['bid']} and total utility: {client['utility']}")
    round_cnt += 1

@app.route('/', methods=['POST'])
def receive_orders():
    data = request.get_data().decode('utf-8')
    print(data) 
    deliver_products(request.json.get('clients'))
    return 'ok', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000, debug=False)
