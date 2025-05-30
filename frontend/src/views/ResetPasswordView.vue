<script setup>
import Content from '../components/resetpasswordpage/Content.vue'

import { inject } from 'vue'
import { useRouter } from 'vue-router'
import { useNotification } from '@kyvg/vue3-notification'

const store = inject("store")
const router = useRouter()
const notification = useNotification()

if (store.state.token) {
  router.push("/")
  notification.notify({ title: 'Reset password not allowed.', text: 'Logout to reset password.' })
}
</script>
<template>
  <Content />
</template>

<style scoped>
</style>
