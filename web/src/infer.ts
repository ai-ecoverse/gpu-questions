/** Browser inference: features → ONNX emissions → CRF → compile. */

import { compileQuestions, type Question } from "./compile";
import { viterbi } from "./crf";
import { NUM_LABELS } from "./labels";
import { ort } from "./ort-wasm";
import {
  FEATURE_ROWS,
  MAX_TOKENS,
  MAX_WIDTH,
  clean,
  featuresV1,
  packRows,
  tailStart,
  tokenize,
  type Token,
} from "./tokenize";

export type ModelBundle = {
  sessions: ort.InferenceSession[];
  start: number[];
  transition: number[][];
  staticVocab: Map<string, number>;
  featureRows: number;
};

export async function loadModel(baseUrl = "/model"): Promise<ModelBundle> {
  const config = await (await fetch(`${baseUrl}/config.json`)).json();
  const crf = await (await fetch(`${baseUrl}/crf.json`)).json();
  const vocabList: string[] = await (await fetch(`${baseUrl}/static_vocab.json`)).json();
  const staticVocab = new Map(vocabList.map((w, i) => [w, i]));
  const sessions: ort.InferenceSession[] = [];
  for (const name of config.onnx as string[]) {
    sessions.push(
      await ort.InferenceSession.create(`${baseUrl}/${name}`, {
        executionProviders: ["wasm"],
      }),
    );
  }
  return {
    sessions,
    start: crf.start,
    transition: crf.transition,
    staticVocab,
    featureRows: config.feature_rows ?? FEATURE_ROWS,
  };
}

async function emissions(bundle: ModelBundle, rows: Int32Array): Promise<Float32Array> {
  const tensor = new ort.Tensor("int64", BigInt64Array.from(Array.from(rows, (x) => BigInt(x))), [
    1,
    MAX_TOKENS,
    MAX_WIDTH,
  ]);
  const outs: Float32Array[] = [];
  for (const sess of bundle.sessions) {
    const result = await sess.run({ rows: tensor });
    const data = result.emissions!.data as Float32Array;
    outs.push(data);
  }
  if (outs.length === 1) return outs[0]!;
  const avg = new Float32Array(outs[0]!.length);
  for (const o of outs) {
    for (let i = 0; i < avg.length; i++) avg[i]! += o[i]!;
  }
  for (let i = 0; i < avg.length; i++) avg[i]! /= outs.length;
  return avg;
}

export async function predict(bundle: ModelBundle, raw: string): Promise<{
  text: string;
  questions: Question[];
  labels: number[];
  tokens: Token[];
  truncated: boolean;
}> {
  const text = clean(raw);
  const all = tokenize(text);
  const start = tailStart(all);
  const tokens = all.slice(start);
  const rows = featuresV1(text, tokens, bundle.staticVocab);
  const packed = packRows(rows, bundle.featureRows);
  const em = await emissions(bundle, packed);
  const stepEm = em.subarray(0, tokens.length * NUM_LABELS);
  const labels = viterbi(stepEm, tokens.length, bundle.start, bundle.transition);
  const questions = compileQuestions(text, tokens, labels);
  return { text, questions, labels, tokens, truncated: start > 0 };
}
