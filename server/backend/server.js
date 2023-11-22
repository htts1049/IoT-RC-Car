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


/*
const connection = createConnection({
  host: process.env.host || "localhost",
  user: process.env.user || "root",
  password: process.env.password || "root",
  database: process.env.database || "infos",
});


connection.connect();
*/

function test(json_data) {
  
  const query = "INSERT INTO your_table_name (forward, backward, leftside, rightside, image, datetime) VALUES ?";
  const values = [[json_data.dist.up, json_data.dist.down, json_data.dist.left, json_data.dist.right, json_data.imageBlob, json_data.dateTime],]
  const data = connection.query(
    query, 
    [values], function (err, result) {
      if (err) throw err;
      console.log("Number of records inserted: " + result.affectedRows);
    }
  );
  console.log(data);
  return data;
}

io.on("connection", (socket) => {

  socket.on("device backend", (json_data) => {
    // console.log(`receive file ${name} from device`);
    
    /*
    writeFile(path.join(__dirname, "dist", "assets", name), file, (err) => {
      callback({ message: err ? "write failure" : "write success" });
    });
    */

    console.log(json_data);

    
    // console.log(test(json_data));
    const dist = {
      up: json_data.dist.up,
      left: json_data.dist.left,
      right: json_data.dist.right,
      down: json_data.dist.down,
    }
    
    console.log(dist);
   
    socket.broadcast.emit("backend frontend", dist);
  })

  socket.on("frontend backend", (command) => {
    console.log(command);
    socket.broadcast.emit("backend device", command);
  });
});

httpServer.listen(port, () =>
  console.log(`server listening at http://localhost:${port}`)
);
