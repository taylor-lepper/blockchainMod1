
import eth_keys, binascii



signature = "0xacd0acd4eabd1bec05393b33b4018fa38b69eba8f16ac3d60eec9f4d2abc127e3c92939e680b91b094242af80fce6f217a34197a69d35edaf616cb0c3da4265b01"
msg = "exercise-cryptography"
msgSigner = '0xa44f70834a711F0DF388ab016465f2eEb255dEd0'

signature= signature[2:]

daSig = eth_keys.keys.Signature(binascii.unhexlify(signature))
encoded = msg.encode("utf8")

print(daSig)
print(encoded)

signerPubKey = daSig.recover_public_key_from_msg(encoded)
print('Signer public key (recovered):', signerPubKey)

signerAddress = signerPubKey.to_checksum_address()

print('Signer address:', signerAddress)
print('Signature valid?:', signerAddress == msgSigner)





