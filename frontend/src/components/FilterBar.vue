<script setup lang="ts">
import Button from "@/primitives/Button.vue";
import {
  deleteAllCompletedTasksMutation,
  getAllTasksQueryKey,
} from "@/shared/client/@tanstack/vue-query.gen";
import type { Filter } from "@/shared/types/types";
import { useMutation, useQueryClient } from "@tanstack/vue-query";
import { computed } from "vue";
import { toast } from "vue3-toastify";

const queryClient = useQueryClient();
const props = defineProps<{
  totalTaskCount: number;
  currentFilter: Filter;
}>();
const emit = defineEmits<{
  filter: [filter: Filter];
}>();

const isSingleTask = computed(() => props.totalTaskCount === 1);

const { mutate } = useMutation({
  ...deleteAllCompletedTasksMutation({
    credentials: "include",
  }),
  onSuccess: () => {
    queryClient.invalidateQueries({
      queryKey: getAllTasksQueryKey({
        credentials: "include",
      }),
    });
    toast.success("All completed tasks cleared successfully");
  },
  onError: () => {
    toast.error("Deletion of all completed tasks failed");
  },
});

const handleClearCompleted = () => {
  if (props.totalTaskCount === 0) {
    toast.warning("No completed tasks left to clear");
    return;
  }

  mutate({});
};
</script>

<template>
  <div class="layout">
    <span>{{ totalTaskCount }} {{ isSingleTask ? "item" : "items" }} left</span>
    <div class="filter-layout">
      <Button
        :class="currentFilter === 'all' ? 'active' : undefined"
        class="ghost"
        @click="emit('filter', 'all')"
        >All</Button
      >
      <Button
        :class="currentFilter === 'active' ? 'active' : undefined"
        class="ghost"
        @click="emit('filter', 'active')"
        >Active</Button
      >
      <Button
        :class="currentFilter === 'completed' ? 'active' : undefined"
        class="ghost"
        @click="emit('filter', 'completed')"
        >Completed</Button
      >
    </div>
    <Button @click="handleClearCompleted" class="ghost">Clear Completed</Button>
  </div>
</template>

<style scoped>
.layout {
  display: grid;
  grid-template-columns: auto 1fr auto;
  gap: 1rem;
  place-items: center;
  padding: 1rem;
  border-radius: 0.5rem;
  background-color: var(--color-background-surface-primary);
}

.filter-layout {
  display: grid;
  gap: 0.5rem;
  grid-template-columns: repeat(3, auto);
  place-content: center;
}
</style>
