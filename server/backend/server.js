const express = require("express");
const path = require("path");
const cors = require("cors");
//const https = require("https");
const { createServer } = require("http");
const { Server } = require("socket.io");
const { writeFile, copyFileSync } = require("fs");

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

/* Code for backend database
const connection = createConnection({
  host: process.env.host || "localhost",
  user: process.env.user || "root",
  password: process.env.password || "root",
  database: process.env.database || "infos",
});

connection.connect();
*/

const getRandomIntInclusive = (min, max) => {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1)) + min; //최댓값도 포함, 최솟값도 포함
};

io.on("connection", (socket) => {
  /* Code for backend database
  socket.on("device backend", (name, file) => {
    console.log(`receive file ${name} from device`);
    writeFile(path.join(__dirname, "dist", "assets", name), file, (err) => {
      callback({ message: err ? "write failure" : "write success" });
    });
    const query = `INSERT INTO ${process.env.table || "images"} VALUES ${name}`;
    connection.query(query, (err, rows, field) => {
      callback({ message: err ? "insert failure" : "insert success" });
    });
  });
  */

  socket.on("frontend backend", (command) => {
    console.log(command);
    socket.broadcast.emit("backend device", command);
  });

  socket.on("device backend", (dist) => {
    console.log(dist);
    //const time = "screen"; // Date.now().toString();
    /* Code for backend frontend
    console.log(path.join(frontPath, "screen.jpg"));
    console.log(path.join(frontPath, time + ".jpg"));
    copyFileSync(
      path.join(frontPath, "screen.jpg"),
      path.join(frontPath, time + ".jpg")
    );
    */
    socket.broadcast.emit("backend frontend", dist);
  });
});

httpServer.listen(port, () =>
  console.log(`server listening at http://localhost:${port}`)
);
