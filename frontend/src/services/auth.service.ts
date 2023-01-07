import { createSignal } from "solid-js";
import type { useNavigate } from "solid-start"
import { getFromLocalStorage } from "./local-storage.service";

export const [getAccessToken, setAccessToken] = createSignal('', {
  name: "accessToken",
});

export function redirectToLoginIfNotLoggedIn(navigate: ReturnType<typeof useNavigate>) {
  if ((getFromLocalStorage('access_token') ?? '').length === 0) {
    navigate('/login');
  }
}

export function redirectToSelectIfLoggedIn(navigate: ReturnType<typeof useNavigate>) {
  if ((getFromLocalStorage('access_token') ?? '').length > 0) {
    navigate('/select');
  }
}