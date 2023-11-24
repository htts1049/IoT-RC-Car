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
    process.env.table || "info"
  } (forward, backward, image, datetime, speed, off) VALUES ?`;
  const values = [
    [...Object.values(json_data.dist), json_data.imageBlob, json_data.dateTime, json_data.speed, json_data.off],
  ];
  connection.query(query, [values], function (err, result) {
    if (err) throw err;
    console.log("Number of records inserted: " + result.affectedRows);
  });
};

io.on("connection", (socket) => {
  socket.on("device backend", (json_data) => {
    insertDB(json_data);
    const threshold = 20;
    const dist = {
      up: json_data.dist.up < threshold,
      left: false,
      right: false,
      down: json_data.dist.down < threshold,
    };

    console.log(json_data);
    socket.broadcast.emit(
      "backend frontend",
      dist,
      json_data.imageBlob,
      json_data.dateTime,
      json_data.speed,
      json_data.off
    );
  });

  socket.on("frontend backend", (command) => {
    socket.broadcast.emit("backend device", command);
  });
});

httpServer.listen(port, () =>
  console.log(`server listening at http://localhost:${port}`)
);
