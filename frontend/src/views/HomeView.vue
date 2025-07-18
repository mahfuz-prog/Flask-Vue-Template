<script setup>
import { onErrorCaptured, ref, inject } from 'vue'
import { viewErrorHandler } from '@/utils/errorHandler'
import { useRouter } from "vue-router"

import Error from '../components/templates/Error.vue'
import Content from '../components/homepage/Content.vue'
import ContentSkeleton from '../components/homepage/ContentSkeleton.vue'

const error = ref("")
const store = inject("store")
const router = useRouter()

const viewErrorHandlerCallback = viewErrorHandler({
  store,
  router,
  errorRef: error
})

// handle error
onErrorCaptured(viewErrorHandlerCallback)
</script>
<template>
  <template v-if="!error">
    <Suspense>
      <template #default>
        <div class="page">
          <Content />
        </div>
      </template>
      <template #fallback>
        <ContentSkeleton />
      </template>
    </Suspense>
  </template>
  <Error :err="String(error)" v-if="error" />
</template>

<style scoped>
.page {
  scrollbar-color: var(--accent) transparent;
  scrollbar-width: thin;
  height: calc(100vh - 65px - 42px);
  display: grid;
  place-items: center;
}
</style>
