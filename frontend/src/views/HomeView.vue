<script setup>
import { onErrorCaptured, ref } from 'vue'
import Error from '../components/templates/Error.vue'
import Content from '../components/homepage/Content.vue'
import ContentSkeleton from '../components/homepage/ContentSkeleton.vue'

const error = ref("")

onErrorCaptured((err) => {
  error.value = err
  return false
})
</script>
<template>
  <template v-if="!error">
    <Suspense>
      <template #default>
        <Content />
      </template>
      <template #fallback>
        <ContentSkeleton />
      </template>
    </Suspense>
  </template>
  <Error :err="String(error)" v-if="error" />
</template>

<style scoped>
</style>
