"use strict";
var CryptoJS = require("crypto-js");
var express = require("express");
var bodyParser = require("body-parser");
var WebSocket = require("ws");

var difficulty = 4;

var http_port = process.env.HTTP_PORT || 3001;
var p2p_port = process.env.P2P_PORT || 6001;
var initialPeers = process.env.PEERS ? process.env.PEERS.split(",") : [];

class Block {
	constructor(index, previousHash, timestamp, data, hash, difficulty, nonce) {
		this.index = index;
		this.previousHash = previousHash.toString();
		this.timestamp = timestamp;
		this.data = data;
		this.hash = hash.toString();
		this.difficulty = difficulty;
		this.nonce = nonce;
	}
}

var getGenesisBlock = () => {
	return new Block(
		0,
		"0",
		1465154705,
		"my genesis block!!",
		"816534932c2b7154836da6afc367695e6337db8a921823784c14378abed4f7d7",
		0,
		0
	);
};

//**** http server ****

//holds the peers
var sockets = [];

//server routes
var initHttpServer = () => {
	var app = express();
	app.use(bodyParser.json());

	app.get("/blocks", (req, res) => res.send(JSON.stringify(blockchain)));
	app.post("/mineBlock", (req, res) => {
		var newBlock = mineBlock(req.body.data);
		// var newBlock = generateNextBlock(req.body.data);
		addBlock(newBlock);
		broadcast(responseLatestMsg());
		console.log("block added: " + JSON.stringify(newBlock));
		res.send();
	});
	app.get("/peers", (req, res) => {
		res.send(
			sockets.map(
				(s) => s._socket.remoteAddress + ":" + s._socket.remotePort
			)
		);
	});
	app.post("addPeer", (req, res) => {
		connect([req.body.peer]);
		res.send();
	});
	app.listen(http_port, () =>
		console.log("Listening http on port: " + http_port)
	);
};

//**** p2p server ****

var initP2PServer = () => {
	var server = new WebSocket.Server({ port: p2p_port });
	server.on("connection", (ws) => initConnection(ws));
	console.log("listening websocket p2p port on: " + p2p_port);
};

//messaging section
var write = (ws, message) => ws.send(JSON.stringify(message));

var MessageType = {
	QUERY_LATEST: 0,
	QUERY_ALL: 1,
	RESPONSE_BLOCKCHAIN: 2,
};

var queryChainLengthMsg = () => ({ type: MessageType.QUERY_LATEST });
var queryAllMsg = () => ({ type: MessageType.QUERY_ALL });
var responseChainMsg = () => ({
	type: MessageType.RESPONSE_BLOCKCHAIN,
	data: JSON.stringify(blockchain),
});
var responseLatestMsg = () => ({
	type: MessageType.RESPONSE_BLOCKCHAIN,
	data: JSON.stringify([getLatestBlock()]),
});

//recieve msg and choose what to do
var handleBlockChainResponse = (message) => {
	var recievedBlocks = JSON.parse(message.data).sort(
		(b1, b2) => b1.index - b2.index
	);
	var latestBlockRecieved = recievedBlocks[recievedBlocks.length - 1];
	var latestBlockHeld = getLatestBlock();
	if (latestBlockRecieved.index > latestBlockHeld.index) {
		console.log(
			"blockchain possibly behind. We got: " +
				latestBlockHeld.index +
				", Peer got: " +
				latestBlockRecieved.index
		);
		if (latestBlockHeld.hash === latestBlockRecieved.previousHash) {
			console.log("We can append the recieved block to our chain");
			addBlock(latestBlockRecieved);
			broadcast(responseLatestMsg());
		} else if (recievedBlocks.length === 1) {
			console.log("We have to query the chain from our peer");
			broadcast(queryAllMsg());
		} else {
			console.log(
				"Recieved blockchain is longer than current blockchain"
			);
			replaceChain(recievedBlocks);
		}
	} else {
		console.log(
			"received blockchain is not longer than current blockchain. Do nothing"
		);
	}
};

//message handler sends JSON strings back to client
var initMessageHandler = (ws) => {
	ws.on("message", (data) => {
		var message = JSON.parse(data);
		console.log("Received message" + JSON.stringify(message));
		switch (message.type) {
			case MessageType.QUERY_LATEST:
				write(ws, responseLatestMsg());
				break;
			case MessageType.QUERY_ALL:
				write(ws, responseChainMsg());
				break;
			case MessageType.RESPONSE_BLOCKCHAIN:
				handleBlockChainResponse(message);
				break;
		}
	});
};

//error handler closes connection and sends message
var initErrorHandler = (ws) => {
	var closeConnection = (ws) => {
		console.log("connection failed to peer: " + ws.url);
		sockets.splice(sockets.indexOf(ws), 1);
	};
	ws.on("close", () => closeConnection(ws));
	ws.on("error", () => closeConnection(ws));
};

//initiation function for peer network
var initConnection = (ws) => {
	sockets.push(ws);
	initMessageHandler(ws);
	initErrorHandler(ws);
	write(ws, queryChainLengthMsg());
};

//broadcasting messages to peers
var broadcast = (message) =>
	sockets.forEach((socket) => write(socket, message));

//initialize connection to peers
var connectToPeers = (newPeers) => {
	newPeers.forEach((peer) => {
		var ws = new WebSocket(peer);
		ws.on("open", () => initConnection(ws));
		ws.on("error", () => {
			console.log("connection failed");
		});
	});
};

//**** blockchain functions ****

var blockchain = [getGenesisBlock()];

var getLatestBlock = () => blockchain[blockchain.length - 1];

var calculateHash = (index, previousHash, timestamp, data, nonce) => {
	return CryptoJS.SHA256(
		index + previousHash + timestamp + data + nonce
	).toString();
};

var calculateHashForBlock = (block) => {
	return calculateHash(
		block.index,
		block.previousHash,
		block.timestamp,
		block.data,
		block.nonce
	);
};

var generateNextBlock = (blockData) => {
	var previousBlock = getLatestBlock();
	var nextIndex = previousBlock.index + 1;
	var nextTimestamp = new Date().getTime() / 1000;
	var nextHash = calculateHash(
		nextIndex,
		previousBlock.hash,
		nextTimestamp,
		blockData
	);
	return new Block(
		nextIndex,
		previousBlock.hash,
		nextTimestamp,
		blockData,
		nextHash
	);
};

var isValidNewBlock = (newBlock, previousBlock) => {
	if (previousBlock.index + 1 !== newBlock.index) {
		console.log("invalid index");
		return false;
	} else if (previousBlock.hash !== newBlock.previousHash) {
		console.log("invalid previous hash");
		return false;
	} else if (calculateHashForBlock(newBlock) !== newBlock.hash) {
		console.log(
			typeof newBlock.hash + " " + typeof calculateHashForBlock(newBlock)
		);
		console.log(
			"invalid hash: " +
				calculateHashForBlock(newBlock) +
				" " +
				newBlock.hash
		);
		return false;
	}
	return true;
};

var addBlock = (newBlock) => {
	if (isValidNewBlock(newBlock, getLatestBlock())) {
		blockchain.push(newBlock);
	}
};

var mineBlock = (blockData) => {
	var previousBlock = getLatestBlock();
	var nextIndex = previousBlock.index + 1;
	var nonce = 0;
	var nextTimestamp = new Date().getTime() / 1000;
	var nextHash = calculateHash(
		nextIndex,
		previousBlock.hash,
		nextTimestamp,
		blockData,
		nonce
	);
	while (
		nextHash.substring(0, difficulty) !== Array(difficulty + 1).join("0")
	) {
		nonce++;
		nextTimestamp = new Date().getTime() / 1000;
		nextHash = calculateHash(
			nextIndex,
			previousBlock.hash,
			nextTimestamp,
			blockData,
			nonce
		);

		console.log(
			'"index"' +
				nextIndex +
				',"previousHash":' +
				previousBlock.hash +
				'"timestamp":' +
				nextTimestamp +
				',"data":' +
				blockData +
				",\x1b[32mhash: " +
				nextHash +
				"\x1b[0m," +
				'"difficulty":' +
				difficulty +
				" \x1b[33mnonce: " +
				nonce +
				" \x1b[0m "
		);
	}
	return new Block(
		nextIndex,
		previousBlock.hash,
		nextTimestamp,
		blockData,
		nextHash,
		difficulty,
		nonce
	);
};

var isValidChain = (blockchainToValidate) => {
	if (
		JSON.stringify(blockchainToValidate[0]) !==
		JSON.stringify(getGenesisBlock())
	) {
		return false;
	}
	var tempBlocks = [blockchainToValidate[0]];
	for (var i = 1; i < blockchainToValidate.length; i++) {
		if (isValidNewBlock(blockchainToValidate[i], tempBlocks[i - 1])) {
			tempBlocks.push(blockchainToValidate[i]);
		} else {
			return false;
		}
	}
	return true;
};

var replaceChain = (newBlocks) => {
	if (isValidChain(newBlocks) && newBlocks.length > blockchain.length) {
		console.log(
			"Recieved blockchain is valid. Replacing current blockchain with recieved blockchain"
		);
		blockchain = newBlocks;
		broadcast(responseLatestMsg());
	} else {
		console.log("Recieved blockchain invalid");
	}
};

//keep at the

//bottom

function testApp() {
	function showBlockchain(inputBLockchain) {
		for (let i = 0; i < inputBLockchain.length; i++) {
			console.log(inputBLockchain[i]);
		}
		console.log();
	}
	// showBlockchain(blockchain);
	// console.log(calculateHashForBlock(getGenesisBlock()));

	//addBlock Test
	// console.log("blockchain before addBlock() execution:");
	// showBlockchain(blockchain);
	// addBlock(generateNextBlock("test block data"));
	// console.log("\n");
	// console.log("blockchain after addBlock() execution:");
	// showBlockchain(blockchain);
}

testApp();

connectToPeers(initialPeers);
initHttpServer();
initP2PServer();
