<script setup>
import { RouterView } from 'vue-router'
import Header from './components/templates/Header.vue'
import Footer from './components/templates/Footer.vue'
</script>
<template>
  <notifications position="top left" classes="notification" />
  <Header />
  <main>
    <RouterView />
  </main>
  <Footer />
</template>

<style>
main {
  height: 100%;
  width: 100%;
}

.vue-notification-group {
  top: 80px !important;
  left: 30px !important;
}

.vue-notification-group .notification {
  color: #fff;
  padding: 10px 15px 10px 15px;
  border-radius: 3px;
  background-color: #000;
  border: 1px solid var(--accent);
}

.vue-notification-group .vue-notification-wrapper {
  margin-top: 10px;
}
</style>
