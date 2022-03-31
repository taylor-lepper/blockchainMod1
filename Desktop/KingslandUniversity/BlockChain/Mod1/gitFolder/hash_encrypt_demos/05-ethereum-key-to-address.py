import eth_keys, binascii


privKey = eth_keys.keys.PrivateKey(binascii.unhexlify(
  '97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a'))
print('Private key (64 hex digits):', privKey)
pubKey = privKey.public_key
print('Public key (plain, 128 hex digits):', pubKey)
pubKeyCompr = '0' + str(2 + int(pubKey) % 2) + str(pubKey)[2:66]
print('Public key (compressed, 66 hex digits):', pubKeyCompr)
address = pubKey.to_checksum_address()
print('Ethereum address:', address)
