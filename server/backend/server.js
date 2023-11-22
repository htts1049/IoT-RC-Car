const express = require("express");
const path = require("path");
const cors = require("cors");
//const https = require("https");
const { createServer } = require("http");
const { Server } = require("socket.io");
const { createConnection } = require("mysql");

require("dotenv").config();

const app = express();

const basePath = path.join(__dirname, "dist");
const frontPath = path.normalize(
  path.join(__dirname, "..", "frontend", "src", "assets")
);
app.use(express.static(basePath));
app.use(cors());
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: "*",
  },
});
const port = process.env.port || 3000;

app.get("/", (req, res) => {
  res.sendFile(path.join(basePath, "index.html"));
});

const connection = createConnection({
  host: process.env.host || "localhost",
  user: process.env.user || "root",
  password: process.env.password || "root",
  database: process.env.database || "car",
});

connection.connect();

const insertDB = (json_data) => {
  const query = `INSERT INTO ${
    process.env.database || "info"
  } (forward, backward, leftside, rightside, image, datetime) VALUES ?`;
  const values = [
    [...Object.values(json_data.dist), json_data.imageBlob, json_data.dateTime],
  ];
  connection.query(query, [values], function (err, result) {
    if (err) throw err;
    console.log("Number of records inserted: " + result.affectedRows);
  });
};

io.on("connection", (socket) => {
  socket.on("device backend", (json_data) => {
    insertDB(json_data);
    const threshold = 10;
    let dist = {};
    for (let d in json_data.dist) {
      dist[d] = json_data.dist[d] < threshold;
    }

    socket.broadcast.emit(
      "backend frontend",
      dist,
      json_data.imageBlob,
      json_data.dateTime
    );
  });

  socket.on("frontend backend", (command) => {
    socket.broadcast.emit("backend device", command);
  });
});

httpServer.listen(port, () =>
  console.log(`server listening at http://localhost:${port}`)
);
