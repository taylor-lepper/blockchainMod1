from pycoin.ecdsa import secp256k1
import hashlib

def keccak_hash(msg) :
  hash_bytes = hashlib.sha3_256(msg.encode("utf8")).digest()
  return int.from_bytes(hash_bytes, byteorder="big")

msg = "some message"
msg_hash = keccak_hash(msg)
private_key = 9999999999999999999999999999999999999999999
signature = secp256k1.Generator.sign(self=secp256k1.secp256k1_generator, secret_exponent=private_key, val=msg_hash)
print("signature = " + str(signature))

public_key = (secp256k1.secp256k1_generator * private_key)
print("public key: " + str(public_key))

valid = secp256k1.Generator.verify(self=secp256k1.secp256k1_generator, public_pair=public_key, val=msg_hash, sig=signature)
print("Signature valid? " + str(valid))

tampered_msg_hash = keccak_hash("tampered msg")
valid = secp256k1.Generator.verify(self=secp256k1.secp256k1_generator, public_pair=public_key, val=tampered_msg_hash, sig=signature)
print("Signature valid? " + str(valid))
