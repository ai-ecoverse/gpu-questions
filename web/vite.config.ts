import { defineConfig } from "vite";

export default defineConfig({
  root: ".",
  publicDir: "public",
  server: {
    port: 5173,
    // Cloudflare quick tunnels / bb connect share hostnames change often.
    allowedHosts: true,
  },
  assetsInclude: ["**/*.wasm", "**/*.onnx"],
  resolve: {
    // Prefer ORT builds that load WASM via wasmPaths instead of embedding it.
    conditions: ["onnxruntime-web-use-extern-wasm", "import", "module", "browser", "default"],
  },
  optimizeDeps: {
    exclude: ["onnxruntime-web"],
  },
  worker: {
    format: "es",
  },
});
