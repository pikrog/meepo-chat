import type { Component } from "solid-js";

import { RouterProvider } from "./router/routes";

export const App: Component = () => {
  return (
    <div class="bg-stone-300">
      <RouterProvider />
    </div>
  );
};
