from flask import Flask, request
from operator import itemgetter
import scrypt
import hashlib
import hmac
import json
import binascii

app =Flask(__name__)

@app.route('/crypto1/sha256', methods=["POST"])
def sha256_endpoint():
    values = request.get_json()

    # check for body
    if not values:
        return "Missing body", 400

    # make sure each msg has a message
    required = ["msg"]
    if not all(k in values for k in required):
        return "Missing values", 400

    # destructure object to get only message value
    message = itemgetter('msg')(values)

    # encode
    encoded = message.encode("utf8")

    # make the hash sha256
    sha256hash = hashlib.sha256(encoded).digest()

    hash = binascii.hexlify(sha256hash)

    # decode to concat
    decoded = hash.decode("utf8")
    decoded = str(decoded)

    # concat to add hex deal
    hexHash = "0x" + decoded

    # send response
    response = {"hash": hexHash}
    # return json.dumps(response), 201

@app.route('/crypto1/sha512', methods=["POST"])
def sha512_endpoint():

    values = request.get_json()
    if not values:
        return "Missing body", 400

    required = ["msg"]
    if not all(k in values for k in required):
        return "Missing values", 400

    # destructure object to get only message value
    message = itemgetter('msg')(values)

    # encode
    encoded = message.encode("utf8")

    # make some hash
    sha512hash = hashlib.sha512(encoded).digest()
    hash = binascii.hexlify(sha512hash)

    # decode to concat
    decoded = hash.decode("utf8")
    decoded = str(decoded)

    # concat to add hex deal
    hexHash = "0x" + decoded
	
    # send response
    response = {"hash": hexHash}

    return response, 201
    # return json.dumps(response), 201

@app.route('/crypto1/ripemd160', methods=["POST"])
def ripemd160_endpoint():

    values = request.get_json()
    if not values:
        return "Missing body", 400

    required = ["msg"]
    if not all(k in values for k in required):
        return "Missing values", 400


    # destructure object to get only message value
    message = itemgetter('msg')(values)

    # encode
    encoded = message.encode("utf8")

    # make some hash
    ripemd160 = hashlib.new('ripemd160', encoded).digest()
    hash = binascii.hexlify(ripemd160)

    # decode to concat
    decoded = hash.decode("utf8")
    decoded = str(decoded)

    # concat to add hex deal
    hexHash = "0x" + decoded
	
    # send response
    response = {"hash": hexHash}
    return response, 201
    # return json.dumps(response), 201

@app.route('/crypto1/hmac', methods=["POST"])
def hmac_endpoint():

    # input body
    values = request.get_json()
    if not values:
        return "Missing body", 400

    required = ["msg", "key"]
    if not all(k in values for k in required):
        return "Missing values", 400

    
    # destructure object to get only message value
    message, key = itemgetter('msg', 'key')(values)

    # encode message
    encoded = message.encode("utf8")
    key = key.encode("utf8")


    # make some hmac and hash
    def hmac_sha256(key, msg):
        return hmac.new(key, msg, hashlib.sha256).digest()

    hash = binascii.hexlify(hmac_sha256(key, encoded))
	
    
    # decode to concat
    decoded = hash.decode("utf8")
    decoded = str(decoded)

    # concat to add hex deal
    hexHash = "0x" + decoded

    # send response
	
    response = {"hmac": hexHash}

    return response, 201
    # return json.dumps(response), 201

@app.route('/crypto1/scrypt', methods=["POST"])
def scrypt_endpoint():
    values = request.get_json()
    if not values:
        return "Missing body", 400

    required = ["password", "salt"]
    if not all(k in values for k in required):
        return "Missing values", 400

    # destructure object to get only message value
    password, salt = itemgetter('password', 'salt')(values)

    # make scrypt
    key = scrypt.hash(password, salt, 16384, 16, 1)
    key = binascii.hexlify(key)

    # decode to concat
    decoded = key.decode("utf8")
    decoded = str(decoded)

    # concat to add hex deal
    hexHash = "0x" + decoded
	
    # return response 
    response = {"key": hexHash}

    return response, 201

    # return json.dumps(response), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)

