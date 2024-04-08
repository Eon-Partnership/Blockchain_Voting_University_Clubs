from flask import Flask, render_template, request
import json
import websockets
import asyncio
from blind_signature_protocol import BlindSignatureProtocol
import os
import sys
from importlib import import_module
from datetime import datetime


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../blockchain')))
from transaction import VoteTransaction

# transaction = import_module('transaction')

# Number of candidates
NUM_CANDIDATES = 4

app = Flask(__name__)

def read_config(filename):
    with open(filename, 'r') as file:
        config = json.load(file)
    return config

async def broadcast_vote_to_miners(message, websocket_uris):
    for uri in websocket_uris:
        async with websockets.connect(uri) as websocket:
            await websocket.send(message)
            print(f"Message sent to: {uri}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vote', methods=['POST'])
def vote_submitted():
    if request.method != 'POST':
        return "Failure"
    
    data = request.json
    token = data.get('token')
    candidate = data.get('candidate')    
    candidate_id = data.get('candidateId')
    print(token, candidate, candidate_id)

    config = read_config("./../resources/config.json")
    ip_addresses = config['ip_addresses']
    ports = config['ports']

    websocket_uris = []
    for i in range(len(ports)):
        uri = "ws://" + ip_addresses[i] + ":" + ports[i]
        websocket_uris.append(uri)

    # Perform Blind-signature protocol
    blindSignatureProtocol = BlindSignatureProtocol()
    t1, t2, t3 = blindSignatureProtocol.perform_alogirthm(token, candidate_id, NUM_CANDIDATES)

    timestamp = int(datetime.now().timestamp())
    # vote_transaction = VoteTransaction(str(t1), str(t2), str(t3), timestamp)

    vote_transaction = {
        "message_type": "vote_transaction",
        "t1": t1,
        "t2": t2,
        "t3": t3,
        "timestamp": timestamp
    }

    vote_transaction_string = json.dumps(vote_transaction)
    
    asyncio.run(broadcast_vote_to_miners(vote_transaction_string, websocket_uris))
    return f"Success!"


if __name__ == '__main__':
    app.run(debug=True, port=8080)