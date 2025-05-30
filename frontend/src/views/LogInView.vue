<script setup>
import Content from '../components/loginpage/Content.vue'

import { inject } from 'vue'
import { useRouter } from 'vue-router'
import { useNotification } from '@kyvg/vue3-notification'

const store = inject("store")
const router = useRouter()
const notification = useNotification()

if (store.state.token) {
  router.push("/")
  notification.notify({ title: 'Log in not allowed.', text: 'You already logged in.' })
}
</script>
<template>
  <Content />
</template>

<style scoped>
</style>
