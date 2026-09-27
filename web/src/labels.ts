/** Token roles — must match gq/labels.py */

export const LABELS = ["O", "Q_B", "Q_I", "OPT_B", "OPT_I", "REC"] as const;
export type Label = (typeof LABELS)[number];
export const NUM_LABELS = LABELS.length;
