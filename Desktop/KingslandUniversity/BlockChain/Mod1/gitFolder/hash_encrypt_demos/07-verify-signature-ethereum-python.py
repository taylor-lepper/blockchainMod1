from bitcoin import privtopub, pubtoaddr



#Create Private Key
private_key = "5HueCGU8rMjxEXxiPuD5BDku4MkFqeZyd4dZ1jvhTVqvbTLvyTJ"
print(private_key)

#Create Public Key

public_key = privtopub(private_key)
print(public_key)

#Create Bitcoin Address
address = pubtoaddr(public_key)
print("My Address is: " + address) 