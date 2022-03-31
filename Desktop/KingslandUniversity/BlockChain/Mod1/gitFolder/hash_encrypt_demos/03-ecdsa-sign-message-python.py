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
