import eth_keys, eth_utils, binascii, os

# privKey = eth_keys.keys.PrivateKey(os.urandom(32))
privKey = eth_keys.keys.PrivateKey(binascii.unhexlify( '97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a'))
pubKey = privKey.public_key
pubKeyCompressed = '0' + str(2 + int(pubKey) % 2) + str(pubKey)[2:66]
address = pubKey.to_checksum_address()
print('Private key (64 hex digits):', privKey)
print('Public key (plain, 128 hex digits):', pubKey)
print('Public key (compressed):', pubKeyCompressed)
print('Signer address:', address)
