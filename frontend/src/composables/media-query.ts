import { onMounted, onUnmounted, ref } from "vue";

export function useMediaQuery(mediaQuery: string) {
  const mediaQueryList = window.matchMedia(mediaQuery);

  const isMediaQueryMatching = ref(mediaQueryList.matches);

  const eventHandler = (event: MediaQueryListEvent) => {
    console.log("is matching: ", event.matches);
    isMediaQueryMatching.value = event.matches;
  };

  onMounted(() => {
    mediaQueryList.addEventListener("change", eventHandler);
  });
  onUnmounted(() => {
    mediaQueryList.removeEventListener("change", eventHandler);
  });

  return { isMediaQueryMatching };
}
