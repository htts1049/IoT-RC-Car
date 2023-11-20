import { reactive } from "vue";
import { io } from "socket.io-client";

export const state = reactive({
  connected: false,
  time: "screen2", //Date.now().toString(),
});

const URL = "http://localhost:3000";

export const socket = io(URL, {
  cors: { origin: "*" },
});

socket.on("connect", () => {
  state.connected = true;
});

socket.on("disconnect", () => {
  state.connected = false;
});

socket.on("backend frontend", (time) => {
  state.time = time.time;
  console.log(state.time);
});
