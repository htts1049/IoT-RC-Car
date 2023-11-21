<script setup>
import { socket, socket_states } from "@/socket.js";
const toggleButton = (event) => {
  event.currentTarget.children[0].classList.toggle("none");
  socket.emit("frontend backend", event.currentTarget.getAttribute("class"));
};
const threshold = 10;
const keys = [
  ["w", "W", "ArrowUp"],
  ["a", "A", "ArrowLeft"],
  ["d", "D", "ArrowRight"],
  ["s", "S", "ArrowDown"],
];
const states = [
  {
    target: "up",
    blocked: false,
    pressed: false,
    keynum: 0,
  },
  {
    target: "left",
    blocked: false,
    pressed: false,
    keynum: 0,
  },
  {
    target: "right",
    blocked: false,
    pressed: false,
    keynum: 0,
  },
  {
    target: "down",
    blocked: false,
    pressed: false,
    keynum: 0,
  },
];

document.addEventListener("keydown", (event) => {
  states.forEach((state, ti) => {
    keys[ti].forEach((key, ki) => {
      if (states[3 - ti].blocked || !states[3 - ti].pressed) {
        if (key === event.key && (state.keynum >> ki) % 2 === 0) {
          state.keynum += 1 << ki;
          if (!state.pressed) {
            state.pressed = true;
            document
              .getElementsByClassName(state.target)[0]
              .children[0].classList.remove("none");
            if (!state.blocked) {
              document
                .getElementsByClassName(state.target)[0]
                .children[0].classList.add("pressed");
              socket.emit("frontend backend", state.target);
            } else {
              document
                .getElementsByClassName(state.target)[0]
                .children[0].classList.add("blocked");
            }
          }
        }
      }
    });
  });
});

document.addEventListener("keyup", (event) => {
  states.forEach((state, ti) => {
    keys[ti].forEach((key, ki) => {
      if (states[3 - ti].blocked || !states[3 - ti].pressed) {
        if (key === event.key && (state.keynum >> ki) % 2 === 1) {
          state.keynum -= 1 << ki;
          if (state.keynum === 0) {
            state.pressed = false;
            document
              .getElementsByClassName(state.target)[0]
              .children[0].classList.add("none");
            if (!state.blocked) {
              document
                .getElementsByClassName(state.target)[0]
                .children[0].classList.remove("pressed");
              socket.emit("frontend backend", `${state.target}_stop`);
            } else {
              document
                .getElementsByClassName(state.target)[0]
                .children[0].classList.remove("blocked");
            }
          }
        }
      }
    });
  });
});

const setStateByDist = (dist, si) => {
  states[si].blocked = dist < threshold;
  if (states[si].blocked) {
    states[si].pressed = false;
    states[si].keynum = 0;
    socket.emit("frontend backend", `${states[si].target}_stop`);
  }
  return states[si].blocked
    ? states[si].pressed
      ? "blocked"
      : "none"
    : states[si].pressed
    ? "pressed"
    : "none";
};
</script>

<template>
  <div class="controller">
    <div class="up" @click="toggleButton">
      <img
        alt="up"
        :class="setStateByDist(socket_states.dist.up, 0)"
        src="../assets/up.svg"
      />
    </div>
    <div class="left" @click="toggleButton">
      <img
        alt="left"
        :class="setStateByDist(socket_states.dist.left, 1)"
        src="../assets/left.svg"
      />
    </div>
    <div class="right" @click="toggleButton">
      <img
        alt="right"
        :class="setStateByDist(socket_states.dist.right, 2)"
        src="../assets/right.svg"
      />
    </div>
    <div class="down" @click="toggleButton">
      <img
        alt="down"
        :class="setStateByDist(socket_states.dist.up, 3)"
        src="../assets/down.svg"
      />
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

.pressed {
  filter: invert(100%) sepia(20%) saturate(186%) hue-rotate(267deg)
    brightness(118%) contrast(100%);
  width: 100%;
  height: 100%;
}

.blocked {
  width: 100%;
  height: 100%;
}
.none {
  display: none;
}
</style>
