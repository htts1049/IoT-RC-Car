<script setup>
import Controller from "./components/Controller.vue";
import { socket_states } from "@/socket.js";
</script>

<template>
  <main>
    <div>
      <img alt="Camera screen" class="camera" :src="socket_states.src" />
      <p class="time">{{ socket_states.time }}</p>
    </div>
    <Controller />
  </main>
</template>

<style scoped>
main {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-column-gap: 10px;
  width: 90%;
  margin: 0 auto;
  padding: 10px;
  background-color: white;
  place-items: center start;
}

.camera {
  width: 100%;
  height: auto;
}

.time {
  text-align: center;
}
</style>
