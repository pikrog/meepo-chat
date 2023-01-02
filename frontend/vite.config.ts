import { defineConfig } from "vite";
import solidPlugin from "vite-plugin-solid";
import dns from 'dns'

dns.setDefaultResultOrder('verbatim');

export default defineConfig({
  plugins: [solidPlugin()],
  server: {
    port: 3000,
  },
});
