<script setup>
defineProps({
  err: String
})
</script>
<template>
  <i><h1>{{ err }}</h1></i>
</template>

<style scoped>
h1 {
  font-weight: 700;
}
</style>
