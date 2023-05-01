const {Account, NodeConnection} = AleoJS

let account = new Account()

// Get the account's address
account.address().to_string()

let connection = new NodeConnection("http://localhost:4130") // Or your node's IP or domain

// Associate the account to the new NodeConnection
connection.setAccount(account)

// Get all the ciphertexts for the setted account
connection.getAllCiphertexts()

// Get and log all the unspent ciphertexts for the setted account
connection.getUnspentCiphertexts().then( (cyphers) => console.log(cyphers))

// Get, decrypt and log all the unspent ciphertexts for the setted account
connection.getUnspentCiphertexts().then( (cyphers) => console.log(account.decryptRecord(cyphers[0]).to_string()))

// Get the node's latest block height
connection.getLatestHeight()

// Get a transaction by its id
connection.getTransaction("at1fjlvusfy8wecaf2487m75y8p2ctvaa3k2s0ucft3jnygm0hwkypq3r6sz7")

// Get a block by its number
connection.getBlock(1)
