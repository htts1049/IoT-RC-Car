import { reactive } from "vue";
import { io } from "socket.io-client";

export const socket_states = reactive({
  connected: false,
  //time: "screen2", //Date.now().toString(),
  dist: {
    up: true,
    left: true,
    right: true,
    down: true,
  },
  src: "/src/assets/screen.jpg",
  time: new Date().toString(),
});

const URL = "http://localhost:3000";

let first = false;

export const socket = io(URL, {
  cors: { origin: "*" },
});

socket.on("connect", () => {
  socket_states.connected = true;
});

socket.on("disconnect", () => {
  socket_states.connected = false;
});

socket.on("backend frontend", (dist, blob, dateTime) => {
  socket_states.dist = dist;
  if (!first) {
    first = true;
  } else {
    window.URL.revokeObjectURL(socket_states.src);
  }
  socket_states.src = window.URL.createObjectURL(blob);
  socket_states.time = dateTime.toString();
});

/*
socket.on("backend frontend", (time) => {
  state.time = time.time;
  console.log(state.time);
});
*/
