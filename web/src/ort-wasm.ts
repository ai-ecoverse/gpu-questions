/** onnxruntime-web WASM backend with Vite-resolved asset URLs (same pattern as cua-s1.js / kev.js).

Import `onnxruntime-web/wasm` (not the default bundle) and point `wasmPaths` at the
threaded SIMD glue via `?url` so Vite serves the `.mjs`/`.wasm` through the module
graph — never from `public/`, which Vite refuses to dynamic-import.
*/

import * as ort from "onnxruntime-web/wasm";
import wasm from "onnxruntime-web/ort-wasm-simd-threaded.wasm?url";
import mjs from "onnxruntime-web/ort-wasm-simd-threaded.mjs?url";

ort.env.wasm.wasmPaths = { wasm, mjs };
// Small model; GitHub Pages also cannot send COOP/COEP for SharedArrayBuffer workers.
ort.env.wasm.numThreads = 1;

export { ort };
