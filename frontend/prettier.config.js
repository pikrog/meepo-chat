/** @type {import('prettier').Config} */
module.exports = {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-call
  plugins: [require("prettier-plugin-tailwindcss")],
  tailwindConfig: "./tailwind.config.js",
};
