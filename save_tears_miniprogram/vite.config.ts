import { defineConfig } from "vite";
import uniPlugin from "@dcloudio/vite-plugin-uni";

const uni = typeof uniPlugin === "function" ? uniPlugin : uniPlugin.default;

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [uni()],
});
