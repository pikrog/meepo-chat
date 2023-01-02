import { createSignal } from "solid-js";

export const [getAccessToken, setAccessToken] = createSignal('', {
  name: "accessToken",
});
