import { reactive } from "vue";
import { io } from "socket.io-client";

export const socket_states = reactive({
  connected: false,
  dist: {
    up: false,
    left: false,
    right: false,
    down: false,
  },
  src: "/src/assets/screen.jpg",
  time: new Date().toString(),
  speed: 0,
  off: false,
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

socket.on("backend frontend", (dist, imageBlob, dateTime, speed, off) => {
  socket_states.dist = dist;
  if (!off) {
    if (!first) {
      first = true;
    } else {
      window.URL.revokeObjectURL(socket_states.src);
    }
    const blob = new Blob([imageBlob], { type: "image/png" });
    socket_states.src = window.URL.createObjectURL(blob);
    socket_states.time = dateTime.toString();
    socket_states.speed = speed;
    socket_states.off = off;
  } else {
    first = false;
    window.URL.revokeObjectURL(socket_states.src);
    socket_states.dist = {
      up: false,
      left: false,
      right: false,
      down: false,
    };
    socket_states.src = "/src/assets/screen.jpg";
    socket.states.time = new Date().toString();
    socket_states.speed = 0;
    socket_states.off = off;
  }
});

/*
socket.on("backend frontend", (time) => {
  state.time = time.time;
  console.log(state.time);
});
*/
