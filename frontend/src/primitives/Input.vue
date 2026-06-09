<script setup lang="ts">
const model = defineModel();
const props = withDefaults(
  defineProps<{
    type?: string;
    class?: string;
  }>(),
  {
    type: "text",
  },
);
</script>

<template>
  <input :type="props.type" :class="props.class" v-model="model" />
</template>

<style scoped>
.text {
  padding: 0.5rem;
  border: none;
  outline: none;
  color: var(--color-text-primary);
  background-color: transparent;

  &.completed {
    text-decoration: line-through;
    color: var(--color-status-disabled);
  }
}

.checkbox {
  --transition-duration: 0.3s;

  appearance: none;
  display: grid;
  place-items: center;
  width: 2rem;
  height: 2rem;
  border: 1px solid;
  border-radius: 50%;
  cursor: pointer;
  background-image: linear-gradient(var(--gradient-from), var(--gradient-to));
  transition:
    --gradient-from var(--transition-duration),
    --gradient-to var(--transition-duration),
    opacity var(--transition-duration);

  &:checked {
    --gradient-from: var(--color-gradient-from);
    --gradient-to: var(--color-gradient-to);

    &:hover {
      opacity: 0.6;
    }

    &:focus {
      /* outline: max(2px, 0.15em) solid currentColor;
      outline-offset: max(2px, 0.15em); */
    }

    &:disabled {
      color: var(--color-text-primary);
      cursor: not-allowed;
    }
  }

  &::before {
    content: "";
    display: block;
    width: 1rem;
    height: 1rem;
    clip-path: polygon(14% 44%, 0 65%, 50% 100%, 100% 16%, 80% 0%, 43% 62%);
    transform: scale(0);
    transition: transform var(--transition-duration);
    background-color: var(--color-background-form-control-primary);
  }

  &:checked::before {
    transform: scale(1);
  }
}
</style>
