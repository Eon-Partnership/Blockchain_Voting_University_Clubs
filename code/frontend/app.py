from flask import Flask, render_template, request
import json
import websockets
import asyncio
from blind_signature_protocol import BlindSignatureProtocol
from helper import read_data_from_file 

#Number of candidates
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
    point, lamba = blindSignatureProtocol.ballot_conformation_algorithm(candidate_id, NUM_CANDIDATES)

    # read the keys
    blindSignatureProtocol.read_keys_of_CA_and_BN()

    # encrypt 



    asyncio.run(broadcast_vote_to_miners("Hi All!", websocket_uris))
    return f"Success!"


if __name__ == '__main__':
    app.run(debug=True, port=8080)