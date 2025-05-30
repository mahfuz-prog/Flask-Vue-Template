<script setup>
import Error from "../components/templates/Error.vue"
import Content from "../components/accountpage/Content.vue"

import { ref, inject, onErrorCaptured } from "vue"
import { useRouter } from "vue-router"
import { useNotification } from "@kyvg/vue3-notification"

const store = inject("store")
const router = useRouter()
const notification = useNotification()

const error = ref("")

if (!store.state.token) {
  router.push("/log-in")
  notification.notify({ title: "Log in required!", text: "Please log in to access this page." })
}

// handle error
onErrorCaptured((err) => {
  error.value = err
  return false
})
</script>
<template>
  <template v-if="!error">
    <Suspense>
      <template #default>
        <Content/>
      </template>
      <template #fallback>
        <span>Loading...</span>
      </template>
    </Suspense>
  </template>
  <Error :err="String(error)" v-if="error" />
</template>

<style scoped>
</style>
