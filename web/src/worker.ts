/** Inference worker: ORT + features + CRF + compile stay off the UI thread. */

import type { Question } from "./compile";
import { loadModel, predict, type ModelBundle } from "./infer";
import "./ort-wasm"; // configure wasmPaths before any InferenceSession.create
import type { Token } from "./tokenize";

export type WorkerIn =
  | { type: "load"; baseUrl: string }
  | { type: "predict"; id: number; text: string };

export type WorkerOut =
  | { type: "ready"; members: number }
  | {
      type: "result";
      id: number;
      text: string;
      questions: Question[];
      labels: number[];
      tokens: Token[];
      truncated: boolean;
      ms: number;
    }
  | { type: "error"; id?: number; message: string };

let bundle: ModelBundle | null = null;

self.onmessage = async (e: MessageEvent<WorkerIn>) => {
  const msg = e.data;
  try {
    if (msg.type === "load") {
      bundle = await loadModel(msg.baseUrl);
      const out: WorkerOut = { type: "ready", members: bundle.sessions.length };
      self.postMessage(out);
      return;
    }
    if (msg.type === "predict") {
      if (!bundle) throw new Error("model not loaded");
      const t0 = performance.now();
      const result = await predict(bundle, msg.text);
      const out: WorkerOut = {
        type: "result",
        id: msg.id,
        text: result.text,
        questions: result.questions,
        labels: result.labels,
        tokens: result.tokens,
        truncated: result.truncated,
        ms: Math.round(performance.now() - t0),
      };
      self.postMessage(out);
    }
  } catch (err) {
    const out: WorkerOut = {
      type: "error",
      id: msg.type === "predict" ? msg.id : undefined,
      message: err instanceof Error ? err.message : String(err),
    };
    self.postMessage(out);
  }
};
