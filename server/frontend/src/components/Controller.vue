<script setup>
import { ref } from "vue";
import { socket, socket_states } from "@/socket.js";

const states = ref([
  {
    target: "up",
    class: "none",
    blocked: false,
    clicked: false,
    pressed: false,
    keys: ["w", "W", "ArrowUp"],
    keynum: 0,
  },
  {
    target: "left",
    class: "none",
    blocked: false,
    clicked: false,
    pressed: false,
    keys: ["a", "A", "ArrowLeft"],
    keynum: 0,
  },
  {
    target: "right",
    class: "none",
    blocked: false,
    clicked: false,
    pressed: false,
    keys: ["d", "D", "ArrowRight"],
    keynum: 0,
  },
  {
    target: "down",
    class: "none",
    blocked: false,
    clicked: false,
    pressed: false,
    keys: ["s", "S", "ArrowDown"],
    keynum: 0,
  },
]);

const clickButton = (event) => {
  let changed = false;
  let message = "";
  let newstate = states.value.map((state, si) => {
    if (state.target === event.currentTarget.className) {
      if (!state.pressed && !state.blocked) {
        if (!state.clicked) {
          if (
            !(
              !states.value[3 - si].blocked &&
              (states.value[3 - si].pressed || states.value[3 - si].clicked)
            )
          ) {
            changed = true;
            if (message !== "") {
              message += " ";
            }
            message += `${state.target}_press`;
            state.class = "pressed";
            state.clicked = true;
          }
        } else {
          changed = true;
          if (message !== "") {
            message += " ";
          }
          message += `${state.target}_stop`;
          state.class = "none";
          state.clicked = false;
        }
      }
    }
    return { ...state };
  });
  if (changed) {
    console.log("click");
    states.value = newstate;
    socket.emit("frontend backend", message);
  }
};

const clickOff = () => {
  socket.emit("frontend backend", "off");
};

document.addEventListener("keydown", (event) => {
  let changed = false;
  let message = "";
  let newstate = states.value.map((state, si) => {
    if (state.keys.includes(event.key)) {
      if (
        !state.clicked &&
        !state.blocked &&
        !(
          !states.value[3 - si].blocked &&
          (states.value[3 - si].pressed || states.value[3 - si].clicked)
        )
      ) {
        const ki = state.keys.findIndex((key) => key === event.key);
        if ((state.keynum >> ki) % 2 === 0) {
          state.keynum += 1 << ki;
          if (!state.pressed) {
            changed = true;
            if (message !== "") {
              message += " ";
            }
            message += `${state.target}_press`;
            state.class = "pressed";
            state.pressed = true;
          }
        }
      }
    }
    return { ...state };
  });
  if (changed) {
    console.log("down");
    socket.emit("frontend backend", message);
    states.value = newstate;
  }
});

document.addEventListener("keyup", (event) => {
  let changed = false;
  let message = "";
  let newstate = states.value.map((state) => {
    if (state.keys.includes(event.key)) {
      const ki = state.keys.findIndex((key) => key === event.key);
      if ((state.keynum >> ki) % 2 === 1) {
        state.keynum -= 1 << ki;
        if (state.keynum === 0 && !state.clicked && !state.blocked) {
          changed = true;
          if (message !== "") {
            message += " ";
          }
          message += `${state.target}_stop`;
          state.class = "none";
          state.pressed = false;
        }
      }
    }
    return { ...state };
  });
  if (changed) {
    console.log("up");
    socket.emit("frontend backend", message);
    states.value = newstate;
  }
});

const setStateByDist = (dist) => {
  let changed = false;
  let message = "";
  let newstate = states.value.map((state) => {
    if (state.pressed || state.clicked) {
      if (dist[state.target] && !state.blocked) {
        changed = true;
        state.blocked = true;
        state.class = "blocked";
        if (message !== "") {
          message += " ";
        }
        message += `${state.target}_stop`;
      } else if (!dist[state.target] && state.blocked) {
        changed = true;
        state.class = "none";
        state.blocked = false;
        state.clicked = false;
        state.pressed = false;
        state.keynum = 0;
      }
    }
    return { ...state };
  });
  if (changed) {
    console.log("set");
    socket.emit("frontend backend", message);
    states.value = newstate;
  }
};
</script>

<template>
  <div class="none">
    {{ setStateByDist(socket_states.dist) }}
  </div>
  <div class="controller">
    <div class="up" @click="clickButton">
      <img alt="up" :class="states[0].class" src="../assets/up.svg" />
    </div>
    <div class="left" @click="clickButton">
      <img alt="left" :class="states[1].class" src="../assets/left.svg" />
    </div>
    <div class="off" @click="clickOff">
      <img alt="off" class="pressed" src="../assets/off.svg" />
    </div>
    <div class="right" @click="clickButton">
      <img alt="right" :class="states[2].class" src="../assets/right.svg" />
    </div>
    <div class="down" @click="clickButton">
      <img alt="down" :class="states[3].class" src="../assets/down.svg" />
    </div>
  </div>
</template>

<style scoped>
.controller {
  display: grid;
  width: 100%;
  height: auto;
  aspect-ratio: 1 / 1;
  grid-template-areas:
    ". up ."
    "left off  right"
    ". down .";
  grid-template-rows: 1fr 1fr 1fr;
  grid-template-columns: 1fr 1fr 1fr;
  grid-gap: 5% 5%;
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

.controller > .off {
  grid-area: off;
  background-color: black;
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
