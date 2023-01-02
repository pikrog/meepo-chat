import { Router } from "@solidjs/router";
import { Component, onMount } from "solid-js";

import { RouterProvider } from "./router/routes";
import { setAccessToken } from "./services/auth.service";
import { setServerAddress } from "./services/chat.service";
import { getEnvars, setMasterServerUrl } from "./services/fetch.service";
import { getFromLocalStorage } from "./services/local-storage.service";

export const App: Component = () => {
  onMount(() => {
    getEnvars().then((envars) => {
      setMasterServerUrl(envars.masterServerAddress);
    })
    setAccessToken(getFromLocalStorage('access_token') ?? '');
    setServerAddress(getFromLocalStorage('server_address') ?? '');
  });

  return (
    <div class="bg-stone-300">
      <Router>
        <RouterProvider />
      </Router>
    </div>
  );
};
