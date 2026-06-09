<script setup lang="ts">
import type { CreateTaskRequest } from "@/shared/client";
import { createTaskMutation, getAllTasksQueryKey } from "@/shared/client/@tanstack/vue-query.gen";
import { useMutation, useQueryClient } from "@tanstack/vue-query";
import { ref } from "vue";
import Input from "@/primitives/Input.vue";
import { toast } from "vue3-toastify";

const queryClient = useQueryClient();

const { mutate } = useMutation({
  ...createTaskMutation({
    credentials: "include",
  }),
  onSuccess: () => {
    queryClient.invalidateQueries({
      queryKey: getAllTasksQueryKey({
        credentials: "include",
      }),
    });
    toast.success(`Task "${form.value.task}" created successfully`);
    form.value.task = "";
  },
  onError: () => {
    toast.error(`Task "${form.value.task}" creation failed`);
  },
});

const form = ref<CreateTaskRequest>({
  is_checked: false,
  task: "",
});

const onSubmit = () => {
  mutate({
    body: form.value,
  });
};
</script>

<template>
  <form @submit.prevent="onSubmit" class="form">
    <Input type="checkbox" class="checkbox" v-model="form.is_checked"></Input>
    <Input type="text" class="text" v-model="form.task" size="30"></Input>
  </form>
</template>

<style scoped>
.form {
  display: grid;
  grid-template-columns: auto 1fr;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 0.375rem;
  background-color: var(--color-background-surface-primary);
}
</style>
