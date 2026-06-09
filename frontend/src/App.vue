<script setup lang="ts">
import { computed, ref, watchEffect } from "vue";
import Button from "@/primitives/Button.vue";
import sunIcon from "./assets/images/icon-sun.svg";
import moonIcon from "./assets/images/icon-moon.svg";
import darkBackgroundDesktop from "./assets/images/bg-desktop-dark.jpg";
import lightBackgroundDesktop from "./assets/images/bg-desktop-light.jpg";
import darkBackgroundMobile from "./assets/images/bg-mobile-dark.jpg";
import lightBackgroundMobile from "./assets/images/bg-mobile-light.jpg";
import { RouterView } from "vue-router";
import { useMediaQuery } from "@/composables/media-query";

type Theme = "light" | "dark";
const currentTheme = ref<Theme>("dark");
const { isMediaQueryMatching } = useMediaQuery("(width >= 768px)");

const isDark = computed(() => currentTheme.value === "dark");
const currentBackgroundImage = computed(() =>
  isMediaQueryMatching.value
    ? isDark.value
      ? darkBackgroundDesktop
      : lightBackgroundDesktop
    : isDark.value
      ? darkBackgroundMobile
      : lightBackgroundMobile,
);

watchEffect(() => {
  const rootElement = document.documentElement;
  const bodyElement = document.body;
  rootElement.classList.remove("light", "dark");
  rootElement.classList.add(currentTheme.value);
  bodyElement.style.backgroundImage = `url(${currentBackgroundImage.value})`;
});

const toggleTheme = () => {
  currentTheme.value = currentTheme.value === "light" ? "dark" : "light";
};
</script>

<template>
  <header class="header">
    <h1>TODO</h1>
    <Button class="icon" @click="toggleTheme">
      <img :src="isDark ? sunIcon : moonIcon" :alt="isDark ? 'sun icon' : 'moon icon'" />
    </Button>
    <!-- <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div> -->
  </header>

  <RouterView />
</template>

<style scoped>
header {
  display: flex;
  justify-content: space-between;
  grid-column: breakout-left-start / breakout-right-end;
  gap: 1rem;
  line-height: 1.5;
  max-height: 100vh;
}

h1 {
  font-size: var(--font-size-heading);
  letter-spacing: 0.5rem;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
