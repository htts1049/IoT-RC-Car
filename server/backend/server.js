// Import necessary modules
const express = require('express');
const http = require('http');
const mysql = require('mysql');
const cors = require("cors");
const { Server } = require('socket.io');

// Create an Express application
const app = express();

app.use(express.json());
app.use(
  cors({
    origin: true
  })
);

const server = http.createServer(app);
const io = new Server(server, {
  cors:{
    origin: true
  }
});

const dbConnection = mysql.createConnection({
  host: 'localhost',
  user: 'root',
  password: 'root',
  database: 'your_database_name'
});

dbConnection.connect();

// WebSocket connection
io.on('connection', (socket) => {
  console.log('Client connected');

  socket.on('deviceData', (data) => {
    console.log(data);
    const deviceData = data;
    const msg = deviceData.deviceData;

    const query = 'INSERT INTO your_table_name (data) VALUES (?)';
    dbConnection.query(query, [msg], (err, result) => {
      if (err) {
        console.error('Error inserting device data:', err);
        return;
      }
      console.log("Inserting device data success.");
      return;
    });

    // Notify connected clients about the new data
    io.emit('newData', msg);

    console.log('Received data from client:', msg);
  });
  // Handle disconnection
  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});

server.listen(3000, () => {
  console.log('Server is running on port 3000');
});