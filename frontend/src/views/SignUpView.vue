<script setup>
import Content from '../components/signuppage/Content.vue'

import { inject } from 'vue'
import { useRouter } from 'vue-router'
import { useNotification } from '@kyvg/vue3-notification'

// reactive store object
const store = inject("store")
const router = useRouter()
const notification = useNotification()

// check if the user already has a jwt token
if (store.state.token) {
  router.push("/")
  notification.notify({ title: "Sign up not allowed.", text: "You are already logged in." })
}
</script>
<template>
  <Content />
</template>

<style scoped>
</style>
