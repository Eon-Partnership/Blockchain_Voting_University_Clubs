from hashlib import sha256

class Transaction():
    def __init__(self, ballot_point, ballot_slope, ballot_signature, timestamp) -> None:        
        # Encrypted candidiate information for a ballot 
        self.ballot_point = ballot_point # Enc(P || H(lambda), PK_BN)
        self.ballot_slope = ballot_slope # Enc(H(ballot_point), SK_CA)
        self.ballot_signature = ballot_signature # Enc(lambda, PK_CA)

        self.timestamp = timestamp
        self.transaction_hash = self.compute_hash()
    
    def compute_hash(self):
        # Concatenating the transaction components to compute a hash
        # ballot_point || ballot_slope || ballot_signature || timestamp
        string_to_hash = self.ballot_point + self.ballot_slope + self.ballot_signature + self.timestamp
        string_to_hash = string_to_hash.encode('utf-8')

        # Computing the hash
        hexDigest = sha256(sha256(string_to_hash)).hexdigest()
        return hexDigest
    