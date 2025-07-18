<script setup>
import { ref, inject } from "vue"

import axios from "axios"

const store = inject("store")

const user = ref({
  userName: null,
  email: null
})

try {
  // get the auth header and include it
  const { data } = await axios.get('users/account/', {
    headers: store.authActions.getAuthorizationHeader()
  })

  // backend name.strip().replace(' ', '-').lower()
  // reverse for showing
  user.value.userName = data.name.replace(/\b\w/g, char => char.toUpperCase()).replace('-', ' ')
  user.value.email = data.email
} catch (err) {
  throw err
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
