<script setup lang="ts">
defineProps<{
  class: string;
}>();
</script>

<template>
  <button class="base" :class="class">
    <slot></slot>
  </button>
</template>

<style scoped>
.base {
  border: none;
  cursor: pointer;
  transition: opacity var(--transition-duration);

  &:hover {
    opacity: 0.3;
  }
}

.icon {
  background-color: transparent;
}
</style>
