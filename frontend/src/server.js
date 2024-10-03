// server.js
const express = require('express');
const { ExpressPeerServer } = require('peer');
const http = require('http');

const app = express();
const server = http.createServer(app);

// Configure PeerJS Server
const peerServer = ExpressPeerServer(server, {
    debug: true,
    path: '/myapp',
});

app.use('/peerjs', peerServer);

// Start the server on port 9000
server.listen(9000, () => {
    console.log('PeerJS server is running at http://localhost:9000/peerjs');
});
