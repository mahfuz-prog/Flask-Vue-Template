<script setup>
import { ref } from 'vue'
import axios from 'axios'
import DocumentationIcon from '../icons/IconDocumentation.vue'

const data = ref("")

try {
  data.value = await (await axios.get('/main/home/')).data

  // handle error
} catch (err) {
  // check the status code of error
  if (err.response) {
    throw new Error(err.response.status)
  } else {
    // general error
    throw new Error(500)
  }
}
</script>
<template>
  <div>
    <DocumentationIcon fill="red" />
    <h4>{{ data }}</h4>
  </div>
</template>

<style scoped>
div {
  width: 200px;
  height: 200px;
  border-radius: 10px;
  background-color: var(--secondary-black);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
}
</style>
