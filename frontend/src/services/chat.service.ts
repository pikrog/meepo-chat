import { createSignal } from "solid-js";

export const [getServerAddress, setServerAddress] = createSignal('', {
  name: "serverAddress",
});
