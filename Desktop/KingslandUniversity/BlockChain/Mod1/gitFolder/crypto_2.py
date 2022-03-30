from flask import Flask, jsonify, request
from operator import itemgetter
import bitcoin, hashlib, binascii, base58
from bitcoin import privtopub, pubtoaddr
import eth_keys, binascii
import json

app =Flask(__name__)
@app.route('/crypto2/eth_sign', methods=["POST"])
def eth_sign():
    values = request.get_json()
    if not values:
        return "Missing body", 400

    required = ["skey", "msg"]
    if not all(k in values for k in required):
        return "Missing values", 400

    # destructure object 
    skey, msg = itemgetter('skey', 'msg')(values)

    # encode and str it
    bMsg = msg.encode("utf8")
    key = str(skey)

    # make a da private key and signature 
    privKey = eth_keys.keys.PrivateKey(binascii.unhexlify(key))
    signature = str(privKey.sign_msg(bMsg))

    # make sure its a str
    msg =str(msg)

    response = {"signature": signature, "msg": msg }

    # return response, 201
    return json.dumps(response), 201

@app.route('/crypto2/eth_sign_to_addr', methods=["POST"])
def eth_sign_to_addr():
    values = request.get_json()
    if not values:
        return "Missing body", 400

    required = ["signature", "msg"]
    if not all(k in values for k in required):
        return "Missing values", 400

    # destructure object 
    signature, msg = itemgetter('signature', 'msg')(values)

    # encode and slice  
    encoded = msg.encode("utf8")
    signature= signature[2:]

    # remake the sig for stupid formatting reasons
    daSig = eth_keys.keys.Signature(binascii.unhexlify(signature))
    
    # get public key from signature and msg
    signerPubKey = daSig.recover_public_key_from_msg(encoded)

    # get address from public key
    signerAddress = signerPubKey.to_checksum_address()

	
    response = {"address": signerAddress}

    # return response, 201
    return json.dumps(response), 201

@app.route('/crypto2/eth_sign_verify', methods=["POST"])
def eth_sign_verify():
    values = request.get_json()
    if not values:
        return "Missing body", 400

    required = ["address", "signature", "msg"]
    if not all(k in values for k in required):
        return "Missing values", 400

    # destructure object 
    address, signature, msg = itemgetter('address', 'signature', 'msg')(values)

    # encode and slice  
    encoded = msg.encode("utf8")
    signature= signature[2:]
    address= str(address)

    # remake the sig for stupid formatting reasons
    daSig = eth_keys.keys.Signature(binascii.unhexlify(signature))
    
    # get public key from signature and msg
    signerPubKey = daSig.recover_public_key_from_msg(encoded)

    # get address from public key
    signerAddress = signerPubKey.to_checksum_address()
	
    # get you boolean
    boo = signerAddress == address
    response = {"valid": boo}
	
    return json.dumps(response), 201

@app.route('/crypto2/btc_skey_to_addr', methods=["POST"])
def btc_skey_to_addr():
    values = request.get_json()
    if not values:
        return "Missing body", 400

    required = ["skey"]
    if not all(k in values for k in required):
        return "Missing values", 400

    # destructure object for private key
    skey = itemgetter('skey')(values)
  

    #Create Public Key
    public_key = privtopub(skey)
    

    #Create Bitcoin Address
    address = pubtoaddr(public_key) 
	
    response = {"address": address}
	
    return json.dumps(response), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

