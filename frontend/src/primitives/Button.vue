<script setup lang="ts">
import type { ButtonHTMLAttributes, ClassValue } from "vue";

const props = withDefaults(
  defineProps<{
    type?: ButtonHTMLAttributes["type"];
    class?: ClassValue;
  }>(),
  {
    type: "button",
  },
);
</script>

<template>
  <button class="base" :class="class" :type="type">
    <slot></slot>
  </button>
</template>

<style scoped>
.base {
  border: none;
  cursor: pointer;
  background-color: transparent;
  transition: opacity var(--transition-duration);

  &:hover {
    opacity: 0.3;
  }
}

.ghost {
  color: var(--color-text-primary);
  background-color: transparent;
}

.active {
  color: var(--color-status-active);
}

.icon {
  background-color: transparent;
}
</style>
