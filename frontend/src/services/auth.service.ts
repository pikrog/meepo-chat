import { createSignal } from "solid-js";
import { User } from "../types";

export const [getGlobalUser, setGlobalUser] = createSignal<null | User>(null, {
  name: "user",
});
