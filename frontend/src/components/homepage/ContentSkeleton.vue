<template>
  <div class="frame">
    <div class="icon"></div>
    <div class="text"></div>
  </div>
</template>

<style scoped>
.frame {
  padding: 20px;
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

.icon {
  width: 21px;
  height: 21px;
  border-radius: 3px;
  animation: pulse-bg 1s infinite;
}

.text {
  width: 100%;
  height: 17px;
  border-radius: 3px;
  animation: pulse-bg 1s infinite;
}

@keyframes pulse-bg {
  0% {
    background-color: var(--tertiary-black);
  }
  50% {
    background-color: rgb(145 145 145 / 64%);
  }
  100% {
    background-color: var(--tertiary-black);
  }
}
</style>
