var elliptic = require('elliptic')
var ec = new elliptic.ec('secp256k1')

// Generate new keypair
const newKeyPair = ec.genKeyPair()
print(newKeyPair)

console.log("---")

// Recover keypair
const privateKey = 'b74efaf103864012b7d692e92385f3eea8ce17f10b269a80762b87da091fbf0d'
const recoveredKeyPair = ec.keyFromPrivate(privateKey)
print(recoveredKeyPair)

// Print utility
function print(keyPair) {
  let publicKey = keyPair.getPublic('hex')
  const publicKeyCompressed = keyPair.getPublic('hex', 'compressed')
  let privateKey = keyPair.getPrivate('hex')
  console.log(`Private key: ${privateKey}`)
  console.log('Public key :', publicKey)
  console.log('Public key (compressed):', publicKeyCompressed)
}