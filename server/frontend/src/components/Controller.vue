<script setup>
import { socket } from "@/socket.js";
const toggleButton = (event) => {
  event.currentTarget.children[0].classList.toggle("none");
  socket.emit("frontend backend", event.currentTarget.getAttribute("class"));
};

const targets = ["up", "left", "right", "down"];
const keys = [
  ["w", "W", "ArrowUp"],
  ["a", "A", "ArrowLeft"],
  ["d", "D", "ArrowRight"],
  ["s", "S", "ArrowDown"],
];
const pressed = [false, false, false, false];

document.addEventListener("keydown", (event) => {
  targets.forEach((value, index) => {
    if (keys[index].includes(event.key) && !pressed[index]) {
      pressed[index] = true;
      document
        .getElementsByClassName(targets[index])[0]
        .children[0].classList.toggle("none");
      socket.emit("frontend backend", value);
    }
  });
});

document.addEventListener("keyup", (event) => {
  targets.forEach((value, index) => {
    if (keys[index].includes(event.key) && pressed[index]) {
      pressed[index] = false;
      document
        .getElementsByClassName(targets[index])[0]
        .children[0].classList.toggle("none");
      socket.emit("frontend backend", `${value}_stop`);
    }
  });
});
</script>

<template>
  <div class="controller">
    <div class="up" @click="toggleButton">
      <img alt="up" class="blocked none" src="../assets/up.svg" />
    </div>
    <div class="left" @click="toggleButton">
      <img alt="left" class="button none" src="../assets/left.svg" />
    </div>
    <div class="right" @click="toggleButton">
      <img alt="right" class="button none" src="../assets/right.svg" />
    </div>
    <div class="down" @click="toggleButton">
      <img alt="down" class="button none" src="../assets/down.svg" />
    </div>
  </div>
</template>

<style scoped>
.controller {
  display: grid;
  width: 100%;
  aspect-ratio: 1;
  grid-template-areas:
    ". up ."
    "left .  right"
    ". down .";
  grid-template-rows: 1fr 1fr 1fr;
  grid-template-columns: 1fr 1fr 1fr;
}
.controller > .up {
  grid-area: up;
  background-color: #8ca0ff;
  border-radius: 50%;
}

.controller > .left {
  grid-area: left;
  background-color: #ffa08c;
  border-radius: 50%;
}

.controller > .right {
  grid-area: right;
  background-color: #ffff64;
  border-radius: 50%;
}

.controller > .down {
  grid-area: down;
  background-color: #8cffa0;
  border-radius: 50%;
}

.button {
  filter: invert(100%) sepia(20%) saturate(186%) hue-rotate(267deg)
    brightness(118%) contrast(100%);
  width: 100%;
}

.blocked {
  filter: none;
  width: 100%;
}
.none {
  display: none;
}
</style>
