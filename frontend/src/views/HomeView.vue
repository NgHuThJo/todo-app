<script setup lang="ts">
import CreateTaskInput from "@/components/CreateTaskInput.vue";
import FilterBar from "@/components/FilterBar.vue";
import Task from "@/components/Task.vue";
import { getAllTasksOptions } from "@/shared/client/@tanstack/vue-query.gen";
import type { Filter } from "@/shared/types/types";
import { useQuery } from "@tanstack/vue-query";
import { computed, ref } from "vue";

const { data, isPending, error } = useQuery({
  ...getAllTasksOptions({
    credentials: "include",
  }),
});
const filter = ref<Filter>("all");

const totalTaskCount = computed(() => data.value?.length ?? 0);
const filteredData = computed(() => {
  if (data.value === undefined) {
    return [];
  }

  switch (filter.value) {
    case "all":
      return data.value;
    case "active":
      return data.value.filter((task) => !task.is_checked);
    case "completed":
      return data.value.filter((task) => task.is_checked);
    default:
      throw Error(`Invalid filter option`);
  }
});
</script>

<template>
  <main class="main">
    <CreateTaskInput />
    <p v-if="isPending">Loading tasks...</p>
    <p v-else-if="error">{{ error?.message }}</p>
    <ul v-else class="list">
      <Task v-for="item in filteredData" :key="item.id" :task="item"></Task>
    </ul>
    <FilterBar
      @filter="(newFilter) => (filter = newFilter)"
      :current-filter="filter"
      :total-task-count="totalTaskCount"
    ></FilterBar>
  </main>
</template>

<style scoped>
.main {
  display: grid;
  justify-content: center;
  gap: 1rem;
}

.list {
  display: grid;

  > *:not(:last-child) {
    border-bottom: 1px solid var(--color-border-primary);
  }

  > *:first-child {
    border-top-left-radius: 0.5rem;
    border-top-right-radius: 0.5rem;
  }
  > *:last-child {
    border-bottom-left-radius: 0.5rem;
    border-bottom-right-radius: 0.5rem;
  }
}
</style>
