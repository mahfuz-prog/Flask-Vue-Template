<script setup>
import axios from "axios"
import { ref, inject } from "vue"
import { useRouter } from "vue-router"
import { useNotification } from "@kyvg/vue3-notification"

const store = inject("store")
const router = useRouter()
const notification = useNotification()

const user = ref({
  userName: null,
  email: null
})

try {
  // get the auth header and include it
  const data = await (await axios.get('users/account/', {
    headers: store.getAuthorizationHeader()
  })).data

  // backend name.strip().replace(' ', '-').lower()
  // reverse for showing
  user.value.userName = data.name.replace(/\b\w/g, char => char.toUpperCase()).replace('-', ' ')
  user.value.email = data.email
} catch (err) {
  // remove the current token, redirect to login page
  if (err.status === 401) {
    store.resetState()
    router.push("log-in/")
  } else {
    throw new Error(500)
  }
}
</script>
<template>
  <div>
    <h4><span>Username: </span>{{ user.userName }}</h4>
    <h4><span>Email: </span>{{ user.email }}</h4>
  </div>
</template>

<style scoped>
span {
  color: #ffffff;
}
</style>
