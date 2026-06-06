import "./assets/main.css";

import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";
import { VueQueryPlugin } from "@tanstack/vue-query";

// Pass the root component here, returns the application instance
const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(VueQueryPlugin);

app.config.errorHandler = (err) => {
  if (err instanceof Error) {
    console.error("An unknown error occurred: ", err);
  }
};

// APPLY ALL APP CONFIGS BEFORE CALLING THE MOUNT FUNCTION
// This function expects an argument which uniquely identifies the DOM element that should
// be used as container for the root component passed above, the argument
// can be a selector string or an actual DOM element
// Note: this function returns the root component, NOT THE APPLICATION INSTANCE
app.mount("#app");
