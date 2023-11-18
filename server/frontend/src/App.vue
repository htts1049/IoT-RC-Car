<template>
  <div id="app">
    <h1>{{ message }}</h1>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import io from 'socket.io-client';

export default {
  setup() {
    const message = ref('Waiting for new data...');

    const socket = io('http://127.0.0.1:3000');

    socket.on('newData', (newData) => {
      message.value = newData;
    });

    onMounted(() => {
      console.log('Component mounted');
    });

    return {
      message
    };
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>