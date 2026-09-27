"""Token roles. Q covers the question sentence, OPT an offered option, REC a default marker."""

LABELS = ["O", "Q_B", "Q_I", "OPT_B", "OPT_I", "REC"]
LABEL_ID = {name: i for i, name in enumerate(LABELS)}
SPAN_KINDS = ("Q", "OPT", "REC")
