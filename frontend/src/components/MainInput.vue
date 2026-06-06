<script setup lang="ts">
import { useMutation } from "@tanstack/vue-query";
import { ref } from "vue";

type Task = {
  isChecked: boolean;
  task: string;
};

const form = ref<Task>({
  isChecked: false,
  task: "",
});

const onSubmit = () => {};
</script>

<template>
  <form @submit.prevent="onSubmit">
    <input type="checkbox" v-model="form.isChecked" />
    <input type="text" v-model="form.task" />
  </form>
</template>

<style scoped></style>
