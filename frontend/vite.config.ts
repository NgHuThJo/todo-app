import { fileURLToPath, URL } from "node:url";

import { heyApiPlugin } from "@hey-api/vite-plugin";
import { defineConfig } from "vite";

import vue from "@vitejs/plugin-vue";
import vueJsx from "@vitejs/plugin-vue-jsx";
import vueDevTools from "vite-plugin-vue-devtools";

// https://vite.dev/config/
export default defineConfig(() => {
  return {
    plugins: [
      vue(),
      vueJsx(),
      vueDevTools(),
      heyApiPlugin({
        config: {
          input: "http://127.0.0.1:8000/openapi.json",
          output: "src/shared/client",
          plugins: ["@tanstack/vue-query"],
        },
        vite: {
          apply: "serve",
        },
      }),
    ],
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
    },
  };
});
