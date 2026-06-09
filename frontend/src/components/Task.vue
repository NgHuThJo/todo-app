<script setup lang="ts">
import {
  deleteTaskMutation,
  getAllTasksQueryKey,
  updateTaskMutation,
} from "@/shared/client/@tanstack/vue-query.gen";
import Input from "@/primitives/Input.vue";
import type { UpdateTaskRequest, GetAllTasksResponse } from "@/shared/client";
import { ref } from "vue";
import { useMutation, useQueryClient } from "@tanstack/vue-query";
import icon_cross from "@/assets/images/icon-cross.svg";
import Button from "@/primitives/Button.vue";
import { toast } from "vue3-toastify";
const props = defineProps<{
  task: GetAllTasksResponse;
}>();

const queryClient = useQueryClient();
const form = ref<UpdateTaskRequest>({
  is_checked: props.task.is_checked,
  task: props.task.task,
});

const { mutate: updateTask } = useMutation({
  ...updateTaskMutation({
    credentials: "include",
  }),
  onSuccess: () => {
    queryClient.invalidateQueries({
      queryKey: getAllTasksQueryKey({
        credentials: "include",
      }),
    });
    toast.success(`Task "${form.value.task}" updated successfully`);
    form.value.task = "";
  },
  onError: () => {
    toast.error(`Task "${form.value.task}" update failed`);
  },
});

const { mutate: deleteTask } = useMutation({
  ...deleteTaskMutation({
    credentials: "include",
  }),
  onSuccess: () => {
    queryClient.invalidateQueries({
      queryKey: getAllTasksQueryKey({
        credentials: "include",
      }),
    });
    toast.success(`Task "${form.value.task}" deletion successful`);
    form.value.task = "";
  },
  onError: () => {
    toast.error(`Task "${form.value.task}" deletion failed`);
  },
});

const handleSubmit = () => {
  console.log("in submit handler");

  updateTask({
    body: form.value,
    path: {
      task_id: props.task.id,
    },
  });
};

const handleDelete = () => {
  console.log("in delete handler");

  deleteTask({
    path: {
      task_id: props.task.id,
    },
  });
};
</script>

<template>
  <form @submit.prevent="handleSubmit" class="form">
    <Input type="checkbox" class="checkbox" v-model="form.is_checked"></Input>
    <Input
      :class="form.is_checked ? 'completed' : undefined"
      type="text"
      class="text"
      v-model="form.task"
      size="30"
    ></Input>
    <Button class="icon" @click="handleDelete">
      <img :src="icon_cross" alt="cross icon" />
    </Button>
  </form>
</template>

<style scoped>
.form {
  display: grid;
  align-items: center;
  grid-template-columns: auto 1fr auto;
  gap: 1rem;
  padding: 1rem;
  background-color: var(--color-background-surface-primary);
}
</style>
