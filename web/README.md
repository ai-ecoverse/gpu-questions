# gpu-ask.js

Agent questions in the browser. Prose in, structured choices out — on-device, nothing sent anywhere.

This folder is the product surface for the tagger trained in the parent `gpu-questions` repo
(gpu-time lineage, ask-tool compiler). Live shape mirrors [kev.js](https://ai-ecoverse.github.io/kev.js/):
docs and demo on one page.

```sh
# From the repo root, after a checkpoint exists:
uv sync --group export
uv run --group export python scripts/export_onnx.py \
  --checkpoint runs/v13-all-a/final.pt,runs/v13-all-b/final.pt \
  --out web/public/model

cd web && npm install && npm run dev
```

Open http://localhost:5173. Inference runs in a Web Worker (ORT WASM + TypeScript CRF/compile).

Planned publish: `@ai-ecoverse/gpu-ask.js` on npm, demo on GitHub Pages, siblings with kev.js and cua-s1.js.
