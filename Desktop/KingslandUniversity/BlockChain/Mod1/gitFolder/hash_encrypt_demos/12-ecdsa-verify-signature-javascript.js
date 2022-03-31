var elliptic = require('elliptic')
var sha3 = require('js-sha3')
var ec = new elliptic.ec('secp256k1')

// var keyPair = ec.genKeyPair(); // Generate random keys
var keyPair = ec.keyFromPrivate(
  '93d154e05084ef67b8c107eb6cd2819570918bd0748d719229441908bc04d133',
)
var privateKey = keyPair.getPrivate('hex')
var publicKey = keyPair.getPublic()
console.log(`Private key: ${privateKey}`)
console.log('Public key :', publicKey.encode('hex').substr(2))
console.log('Public key (compressed):', publicKey.encodeCompressed('hex'))

var message = 'Kingsland University'
var messageHash = sha3.keccak256(message)
var signature = ec.sign(messageHash, privateKey, 'hex', { canonical: true })

console.log(`Msg: ${message}`)
console.log(`Msg hash: ${messageHash}`)
console.log('Signature:', signature.toDER('hex'))

let hexToDecimal = (x) => ec.keyFromPrivate(x, 'hex').getPrivate().toString(10)
let pubKeyRecovered = ec.recoverPubKey(
  hexToDecimal(messageHash),
  signature,
  signature.recoveryParam,
  'hex',
)
console.log('Recovered pubKey:', pubKeyRecovered.encodeCompressed('hex'))
let validSig = ec.verify(messageHash, signature, pubKeyRecovered)
console.log('Signature valid?', validSig)
