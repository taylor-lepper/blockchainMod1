from pure25519 import ed25519_oop
privKey, pubKey = ed25519_oop.create_keypair()
print("Private key (32 bytes):", privKey.to_ascii(encoding='hex'))
print("Public key (32 bytes): ", pubKey.to_ascii(encoding='hex'))
msg = b'Message for signing'
signature = privKey.sign(msg, encoding='hex')
print("Signature (64 bytes):", signature)
try:
    pubKey.verify(signature, msg, encoding='hex')
    print("The signature is valid.")
except:
    print("Invalid signature!")
