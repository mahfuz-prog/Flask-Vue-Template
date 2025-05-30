<script setup>
import { ref, inject, watch } from 'vue'
import { useNotification } from '@kyvg/vue3-notification'
import { useRoute, useRouter, RouterView } from 'vue-router'

const store = inject("store")
const route = useRoute()
const router = useRouter()
const notification = useNotification()


// log out functionality
function logOut() {
  store.resetState()

  // redirect the same route, this will force to reload the route
  router.go(route.fullPath)
  notification.notify({ title: 'Signed out.', text: 'Now you have limited access.' })
}
</script>
<template>
  <header>
    <div>
      <RouterLink to="/"><img alt="Site logo" class="logo" src="@/assets/logo.png" /></RouterLink>
    </div>
    <div class="wrapper">
      <nav v-if="store.state.token">
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/account">Account</RouterLink>
        <button @click="logOut">Log Out</button>
      </nav>
      <nav v-else>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/sign-up">Sign Up</RouterLink>
        <RouterLink to="/log-in">Log In</RouterLink>
      </nav>
    </div>
  </header>
</template>

<style scoped>
header {
  height: 65px;
  padding: 10px 10px 10px 10px;
  width: 1140px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: var(--secondary-black);
}

nav {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 30px;
}

.logo {
  width: 220px;
}

.router-link-active {
  color: var(--accent);
}

img {
  margin-bottom: -6px;
}

button {
  background-color: var(--accent);
  border: 0;
  padding: 8px 35px 8px 35px;
  border-radius: 25px;
  color: #ffffff;
  cursor: pointer;
}

@media (min-width: 768px) {
  header {
    padding: 10px 20px 10px 20px;
    width: 100%;
  }
}
</style>
