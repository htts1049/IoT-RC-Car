<script setup>
import { ref } from "vue";
import { socket, socket_states } from "@/socket.js";
const toggleButton = (event) => {
  event.currentTarget.children[0].classList.toggle("none");
  socket.emit("frontend backend", event.currentTarget.getAttribute("class"));
};
const threshold = 10;

let lock = false;

const states = ref([
  {
    target: "up",
    keys: ["w", "W", "ArrowUp"],
    blocked: false,
    pressed: false,
    keynum: 0,
    class: "none",
  },
  {
    target: "left",
    keys: ["a", "A", "ArrowLeft"],
    blocked: false,
    pressed: false,
    keynum: 0,
    class: "none",
  },
  {
    target: "right",
    keys: ["d", "D", "ArrowRight"],
    blocked: false,
    pressed: false,
    keynum: 0,
    class: "none",
  },
  {
    target: "down",
    keys: ["s", "S", "ArrowDown"],
    blocked: false,
    pressed: false,
    keynum: 0,
    class: "none",
  },
]);

document.addEventListener("keydown", (event) => {
  let changed = false;
  let message = "";
  lock = true;
  console.log("down");
  let newstate = states.value.map((state, ti) => {
    if (states.value[3 - ti].blocked || !states.value[3 - ti].pressed) {
      if (state.keys.includes(event.key)) {
        let ki = state.keys.findIndex((key) => key === event.key);
        if ((state.keynum >> ki) % 2 === 0) {
          state.keynum += 1 << ki;
          if (!state.pressed) {
            changed = true;
            state.pressed = true;
            if (!state.blocked) {
              message += `${state.target}_press `;
              state.class = "pressed";
            } else {
              message += `${state.target}_block `;
              state.class = "blocked";
            }
          }
        }
      }
    }
    return { ...state };
  });
  if (changed) {
    console.log(newstate);
    console.log(message);
    states.value = newstate;
    socket.emit("frontend backend", message);
  }
});

document.addEventListener("keyup", (event) => {
  let changed = false;
  let message = "";

  console.log("up");
  let newstate = states.value.map((state) => {
    if (state.keys.includes(event.key)) {
      let ki = state.keys.findIndex((key) => key === event.key);
      if ((state.keynum >> ki) % 2 === 1) {
        state.keynum -= 1 << ki;
        if (state.keynum === 0) {
          changed = true;
          state.pressed = false;
          message += `${state.target}_stop `;
          state.class = "none";
        }
      }
    }
    return { ...state };
  });
  if (changed) {
    console.log(newstate);
    console.log(message);
    states.value = newstate;
    socket.emit("frontend backend", message);
  }
});

const setStateByDist = (dist) => {
  console.log("set");
  console.log(states.value);
  console.log(dist);
  let changed = false;
  let message = "";
  let newstate = states.value.map((state, si) => {
    if (state.pressed) {
      if (dist[state.target] < threshold && !state.blocked) {
        changed = true;
        message += `${state.target}_blocked `;
        state.blocked = true;
        state.class = "blocked";
      } else if (dist[state.target] >= threshold && state.blocked) {
        changed = true;
        message += `${state.target}_pressed `;
        state.blocked = false;
        state.class = "pressed";
      }
    }
    return { ...state };
  });
  if (changed) {
    console.log(newstate);
    states.value = newstate;
    console.log(states.value);
    //socket.emit("frontend backend", message);
  }
};
</script>

<template>
  <div class="none">
    {{ setStateByDist(socket_states.dist) }}
  </div>
  <div class="controller">
    <div class="up" @click="toggleButton">
      <img alt="up" :class="states[0].class" src="../assets/up.svg" />
    </div>
    <div class="left" @click="toggleButton">
      <img alt="left" :class="states[1].class" src="../assets/left.svg" />
    </div>
    <div class="right" @click="toggleButton">
      <img alt="right" :class="states[2].class" src="../assets/right.svg" />
    </div>
    <div class="down" @click="toggleButton">
      <img alt="down" :class="states[3].class" src="../assets/down.svg" />
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
