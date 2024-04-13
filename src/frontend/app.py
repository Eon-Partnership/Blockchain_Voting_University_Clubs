from flask import Flask, render_template, request
import json
import websockets
import asyncio
from .blind_signature_protocol import BlindSignatureProtocol
from datetime import datetime

# Number of candidates
NUM_CANDIDATES = 4

app = Flask(__name__)

def read_config(filename):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config

async def broadcast_message_to_miners(message, websocket_uris):
    for uri in websocket_uris:
        async with websockets.connect(uri) as websocket:
            await websocket.send(message)
            print(f"Message sent to: {uri}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def see_results():
    if request.method != 'POST':
        return "Failure"

    config = read_config("./../resources/config.json")
    ip_addresses = config['ip_addresses']
    ports = config['ports']

    websocket_uris = []
    for i in range(len(ports)):
        uri = "ws://" + ip_addresses[i] + ":" + ports[i]
        websocket_uris.append(uri)
    
    message = {
        "message_type": "election_results"
    }

    message_string = json.dumps(message)
    
    asyncio.run(broadcast_message_to_miners(message_string, websocket_uris))
    return f"Success!"

@app.route('/vote', methods=['POST'])
def vote_submitted():
    if request.method != 'POST':
        return "Failure"
    
    data = request.json
    token = data.get('token')
    candidate = data.get('candidate')    
    candidate_id = data.get('candidateId')
    print(f"Data received from voting interface: {token=}, {candidate=}, {candidate_id=}")

    config = read_config("./../resources/config.json")
    ip_addresses = config['ip_addresses']
    ports = config['ports']

    websocket_uris = []
    for i in range(len(ports)):
        uri = "ws://" + ip_addresses[i] + ":" + ports[i]
        websocket_uris.append(uri)

    # Perform Blind-signature protocol
    blindSignatureProtocol = BlindSignatureProtocol()
    t1, t2, t3 = blindSignatureProtocol.perform_algorithm(token, candidate_id, NUM_CANDIDATES)

    timestamp = int(datetime.now().timestamp())

    vote_transaction = {
        "message_type": "vote_transaction",
        "t1": t1,
        "t2": t2,
        "t3": t3,
        "timestamp": timestamp
    }

    vote_transaction_string = json.dumps(vote_transaction)
    
    asyncio.run(broadcast_message_to_miners(vote_transaction_string, websocket_uris))
    return f"Success!"


if __name__ == '__main__':
    app.run(debug=True, port=8080)