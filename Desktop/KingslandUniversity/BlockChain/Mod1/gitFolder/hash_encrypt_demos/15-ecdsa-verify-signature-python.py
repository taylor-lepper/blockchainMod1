import eth_keys, eth_utils, binascii, os

# privKey = eth_keys.keys.PrivateKey(os.urandom(32))
privKey = eth_keys.keys.PrivateKey(binascii.unhexlify(
    '97ddae0f3a25b92268175400149d65d6887b9cefaf28ea2c078e05cdc15a3c0a'))
pubKey = privKey.public_key
pubKeyCompressed = '0' + str(2 + int(pubKey) % 2) + str(pubKey)[2:66]
address = pubKey.to_checksum_address()
print('Private key (64 hex digits):', privKey)
print('Public key (plain, 128 hex digits):', pubKey)
print('Public key (compressed, 66 hex digits):', pubKeyCompressed)
print('Signer address:', address)

print()

msg = b'Message for signing'
signature = privKey.sign_msg(msg)
print('Msg:', msg)
print('Msg hash:', binascii.hexlify(eth_utils.keccak(msg)))
print('Signature: [v = {0}, r = {1}, s = {2}]'.format(
    hex(signature.v), hex(signature.r), hex(signature.s)))
print('Signature (130 hex digits):', signature)

print()

msg = b'Message for signing'
msgSigner = '0xa44f70834a711F0DF388ab016465f2eEb255dEd0'
signature = eth_keys.keys.Signature(binascii.unhexlify(
    '6f0156091cbe912f2d5d1215cc3cd81c0963c8839b93af60e0921b61a19c54300c71006dd93f3508c432daca21db0095f4b16542782b7986f48a5d0ae3c583d401'))
signerRecoveredPubKey = signature.recover_public_key_from_msg(msg)
signerRecoveredAddress = signerRecoveredPubKey.to_checksum_address()
print('Signer public key (128 hex digits):', signerRecoveredPubKey)
print('Signer address:', signerRecoveredAddress)
print('Signature valid?:', signerRecoveredAddress == msgSigner)