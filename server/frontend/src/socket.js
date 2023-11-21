import { reactive } from "vue";
import { io } from "socket.io-client";

export const socket_states = reactive({
  connected: false,
  //time: "screen2", //Date.now().toString(),
  dist: {
    up: 20,
    left: 20,
    right: 20,
    down: 20,
  },
});

const URL = "http://localhost:3000";

export const socket = io(URL, {
  cors: { origin: "*" },
});

socket.on("connect", () => {
  socket_states.connected = true;
});

socket.on("disconnect", () => {
  socket_states.connected = false;
});

socket.on("backend frontend", (dist) => {
  socket_states.dist = dist;
  console.log(socket_states.dist);
});

/*
socket.on("backend frontend", (time) => {
  state.time = time.time;
  console.log(state.time);
});
*/
