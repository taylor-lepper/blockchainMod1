import eth_keys, binascii

msg = 'exercise-cryptography'
address= "0xa44f70834a711F0DF388ab016465f2eEb255dEd0"

signature= "0xacd0acd4eabd1bec05393b33b4018fa38b69eba8f16ac3d60eec9f4d2abc127e3c92939e680b91b094242af80fce6f217a34197a69d35edaf616cb0c3da4265b01"

# encode
msg= msg.encode("utf8")
signature= signature[2:]

daSig =eth_keys.keys.Signature(binascii.unhexlify(signature))

print(daSig)