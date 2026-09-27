import random

import pytest
import torch

from gq.compile import compile_questions
from gq.data import Builder, Generator, Sample, encode, last_question_span
from gq.labels import LABEL_ID, LABELS
from gq.model import Ensemble, Tagger, affine_scan, collate
from gq.predict import load, parse
from gq.tokenize import FEATURE_ROWS, clean, features, tokenize


def test_clean_replaces_code_and_urls():
    text = clean("See https://example.com/x?y=1\n```js\nconst a = b ? c : d\n```\nOk?")
    assert "[URL]" in text and "[CODE]" in text
    assert text.count("?") == 1


def test_feature_rows_in_range():
    text = "Done.\n\n- item one\n- item two\n\nWhich one do you want?"
    tokens = tokenize(text)
    rows = features(text, tokens)
    assert len(rows) == len(tokens)
    assert all(0 <= r < FEATURE_ROWS for row in rows for r in row)


def test_last_question_span_skips_abbreviations_and_markers():
    text = "Fixed it.\n2. Should I also bump e.g. the lockfile?"
    start, end = last_question_span(text)
    assert text[start:end] == "Should I also bump e.g. the lockfile?"


def test_encode_assigns_begin_and_inside():
    b = Builder()
    b.add("Want me to ")
    start = len(b.text) - len("Want me to ")
    b.add("fix it", "OPT")
    b.add(" or ")
    b.add("leave it", "OPT")
    b.add("?")
    b.mark(start, "Q")
    tokens, _, labels = encode(Sample(b.text, b.spans))
    names = [LABELS[i] for i in labels]
    assert names[0] == "Q_B"
    assert names[tokens.index(next(t for t in tokens if t.text == "fix"))] == "OPT_B"
    assert names[tokens.index(next(t for t in tokens if t.text == "leave"))] == "OPT_B"


def test_compile_list_before_question():
    text = "Options:\n1. Merge now (recommended)\n2. Wait for CI\n\nWhich one?"
    tokens = tokenize(text)
    labels = [LABEL_ID["O"]] * len(tokens)

    def tag(word, name):
        labels[[t.text for t in tokens].index(word)] = LABEL_ID[name]

    tag("Merge", "OPT_B"); tag("now", "OPT_I"); tag("recommended", "REC")
    tag("Wait", "OPT_B"); tag("for", "OPT_I"); tag("CI", "OPT_I")
    tag("Which", "Q_B"); tag("one", "Q_I"); tag("?", "Q_I")
    [q] = compile_questions(text, tokens, labels)
    assert q.kind == "either_or"
    assert q.options == ["Merge now", "Wait for CI"]
    assert q.default == 0


def test_compile_yes_no_and_open():
    for text, kind, propose in [("Want me to push it?", "yes_no", True), ("Which branch is it on?", "open", False)]:
        tokens = tokenize(text)
        labels = [LABEL_ID["Q_B"]] + [LABEL_ID["Q_I"]] * (len(tokens) - 1)
        [q] = compile_questions(text, tokens, labels)
        assert (q.kind, q.propose) == (kind, propose)


def test_compile_drops_fragment_without_question_mark():
    text = "Deployed to staging. What did you have in mind?"
    tokens = tokenize(text)
    labels = [LABEL_ID["O"]] * len(tokens)
    labels[0], labels[1] = LABEL_ID["Q_B"], LABEL_ID["Q_I"]
    start = [t.text for t in tokens].index("What")
    labels[start] = LABEL_ID["Q_B"]
    for i in range(start + 1, len(tokens)):
        labels[i] = LABEL_ID["Q_I"]
    [q] = compile_questions(text, tokens, labels)
    assert q.prompt == "What did you have in mind?" and q.kind == "open"


def test_compile_cleans_option_markup():
    text = "1. **Full approach**: build it (recommended)\n2. Skip it\n\nWhich one?"
    tokens = tokenize(text)
    labels = [LABEL_ID["O"]] * len(tokens)
    words = [t.text for t in tokens]
    for i in range(words.index("*"), words.index("(") + 3):
        labels[i] = LABEL_ID["OPT_I"]
    labels[words.index("*")] = LABEL_ID["OPT_B"]
    labels[words.index("Skip")], labels[words.index("Skip") + 1] = LABEL_ID["OPT_B"], LABEL_ID["OPT_I"]
    labels[words.index("Which")] = LABEL_ID["Q_B"]
    labels[words.index("Which") + 1] = labels[words.index("Which") + 2] = LABEL_ID["Q_I"]
    [q] = compile_questions(text, tokens, labels)
    assert q.options == ["Full approach: build it", "Skip it"]


def test_is_proposal():
    from gq.compile import is_proposal

    for yes in ("Want me to push it?", "Want a diff?", "Would you like a walkthrough of the parser?",
                "Shall I rename it?", "Voulez-vous que je corrige ce bug ?", "Sound right?", "Need help with the setup?"):
        assert is_proposal(yes), yes
    for no in ("How can I help you today?", "Which module should I work on?", "What would you like me to solve?",
               "Do you want the repo to be public or private?", "Could you share the log?"):
        assert not is_proposal(no), no


def test_is_open_information_requests():
    from gq.compile import is_open

    for yes in ("If so, what site code did you pick?", "Now, to check your order, could you please provide the order ID?",
                "Do you remember the repo directory or approximate date?", "Do you have the dataset ID handy?",
                "Can you check those URLs while logged in and share the class lists?", "Do you know what the URL is?",
                "Could you rephrase what you're trying to say?", "Quel nom tu veux donner au nouveau repo ?",
                "有什么我可以帮你的吗？", "Any thoughts on the open questions?"):
        assert is_open(yes), yes
    for no in ("Want me to push it?", "Do you have access to another machine?", "Could you try running it again?",
               "Should I also update the docs?", "Is this OK?"):
        assert not is_open(no), no


def test_options_match_accepts_explanations_but_not_different_choices():
    from gq.evaluate import options_match

    assert options_match(["vhs", "Cmd+Shift+5"],
                         ["recommendation: vhs for scripted demos", "Cmd+Shift+5` for quick one-off recordings"])
    assert options_match(["`--save` flag", "`--temp` flag"], ["--save` flag to save to file", "--temp` flag to /tmp"])
    assert not options_match(["vhs", "Cmd+Shift+5"], ["vhs"])
    assert not options_match(["keep it", "delete it"], ["keep it or delete it", "delete it"])
    assert not options_match(["Option A", "Option B"], ["Option A: fast", "Option B and Option A"])


def test_clean_option_drops_recommendation_label_and_stray_backtick():
    from gq.compile import _clean_option

    assert _clean_option("recommendation: vhs for demos") == "vhs for demos"
    assert _clean_option("Cmd+Shift+5` for quick recordings") == "Cmd+Shift+5 for quick recordings"
    assert _clean_option("`gh pr create` now") == "`gh pr create` now"
    assert _clean_option("`main`") == "main"
    assert _clean_option("run `make` then `test`") == "run `make` then `test`"


def test_affine_scan_matches_sequential():
    gate, cand = torch.rand(2, 9, 3), torch.randn(2, 9, 3)
    state, expected = torch.zeros(2, 3), []
    for t in range(9):
        state = gate[:, t] * state + cand[:, t]
        expected.append(state)
    assert torch.allclose(affine_scan(gate, cand), torch.stack(expected, 1), atol=1e-5)


def test_crf_nll_and_decode_shapes():
    model = Tagger(hidden=8, layers=1)
    text = "Should I merge it or wait?"
    tokens = tokenize(text)
    rows = features(text, tokens)
    batch = [(rows, [0] * len(rows)), (rows[:3], [0] * 3)]
    r, l, m = collate(batch, "cpu")
    emissions = model.emissions(r, m)
    assert torch.isfinite(model.nll(emissions, l, m))
    paths = model.decode(emissions, m)
    assert [len(p) for p in paths] == [len(rows), 3]


def test_decode_kbest_includes_top1():
    from gq.model import kbest_paths

    model = Tagger(hidden=8, layers=1)
    text = "Should I merge it or wait?"
    tokens = tokenize(text)
    rows = features(text, tokens)
    r, _, m = collate([(rows, [0] * len(rows))], "cpu")
    emissions = model.emissions(r, m)
    top1 = model.decode(emissions, m)[0]
    scored = model.decode_kbest(emissions, m, k=5)[0]
    assert len(scored) == 5
    assert scored[0][1] == top1
    assert scored[0][0] >= scored[-1][0]
    # Shared helper matches the method for a single sequence.
    n = int(m[0].sum())
    assert kbest_paths(emissions[0, :n], model.start.detach(), model.transition.detach(), 5)[0][1] == top1


def test_kind_head_rerank_picks_a_path():
    from gq.predict import parse

    model = Tagger(hidden=8, layers=1, kind_head=True)
    out = parse(model, "Want me to merge it, or wait?", kind_mode="rerank", rerank_k=4)
    assert isinstance(out, list)


def test_constrained_rerank_keeps_top1_negative():
    """If the best CRF path has no question, lower paths must not invent one."""
    from gq.predict import rerank_path

    model = Tagger(hidden=8, layers=1, kind_head=True)
    text = "Deployed to staging. All green."
    tokens = tokenize(text)
    rows = features(text, tokens)
    r, _, m = collate([(rows, [0] * len(rows))], "cpu")
    joined = model.hidden(r, m)
    emissions = model.emissions_from(joined)
    # Force top-1 to be all-O so compile finds nothing; k-best may still have Q tags.
    with torch.no_grad():
        emissions = emissions.clone()
        emissions[0, :, 0] = 10.0  # O
        emissions[0, :, 1:] = -10.0
    qs = rerank_path(model, text, tokens, joined, emissions[0], m[0], k=5, lam=1.0)
    assert qs == []


def test_static_word_vectors_roundtrip(tmp_path):
    from gq.tokenize import STATIC_OFFSET, set_static_vocab

    vocab = ["merge", "wait"]
    set_static_vocab(vocab)
    try:
        text = "Should I merge it or wait?"
        rows = features(text, tokenize(text))
        assert rows[2][-1] == STATIC_OFFSET + 0 and rows[0][-1] == STATIC_OFFSET + len(vocab)
        model = Tagger(hidden=8, layers=1, static_size=len(vocab), static_dim=4)
        model.static_table[: len(vocab)] = torch.randn(len(vocab), 4)
        r, _, m = collate([(rows, [0] * len(rows))], "cpu")
        assert torch.isfinite(model.emissions(r, m)).all()
        path = tmp_path / "s.pt"
        torch.save({"config": model.config, "state": model.state_dict(), "static_vocab": vocab}, path)
        assert parse(load(str(path)), text) is not None
    finally:
        set_static_vocab(None)


@pytest.mark.parametrize("attn_first", [False, True])
def test_attention_ignores_padding_and_roundtrips(tmp_path, attn_first):
    torch.manual_seed(0)
    model = Tagger(hidden=8, layers=1, attn=2, attn_first=attn_first).eval()
    for layer in model.attention:
        torch.nn.init.normal_(layer.out.weight, std=0.5)
    text = "Should I merge it or wait?"
    rows = features(text, tokenize(text))
    r, l, m = collate([(rows, [0] * len(rows)), (rows[:3], [0] * 3)], "cpu")
    emissions = model.emissions(r, m)
    assert torch.isfinite(model.nll(emissions, l, m))
    assert [len(p) for p in model.decode(emissions, m)] == [len(rows), 3]
    alone_r, _, alone_m = collate([(rows[:3], [0] * 3)], "cpu")
    assert torch.allclose(model.emissions(alone_r, alone_m)[0], emissions[1, :3], atol=1e-5)
    path = tmp_path / "a.pt"
    torch.save({"config": model.config, "state": model.state_dict()}, path)
    loaded = load(str(path))
    assert loaded.config["attn"] == 2 and loaded.config.get("attn_first", False) == attn_first
    assert torch.allclose(loaded.emissions(r, m), emissions)
    plain = tmp_path / "p.pt"
    torch.save({"config": Tagger(hidden=8, layers=1).config, "state": Tagger(hidden=8, layers=1).state_dict()}, plain)
    assert isinstance(parse(load(f"{path},{plain}"), text), list)


def test_load_and_parse_ensemble(tmp_path):
    paths = []
    for seed in (1, 2):
        torch.manual_seed(seed)
        model = Tagger(hidden=8, layers=1)
        path = tmp_path / f"m{seed}.pt"
        torch.save({"config": model.config, "state": model.state_dict()}, path)
        paths.append(str(path))
    ensemble = load(",".join(paths))
    assert isinstance(ensemble, Ensemble) and len(ensemble.members) == 2
    assert isinstance(parse(ensemble, "Should I merge it or wait?"), list)


def test_hand_split_is_disjoint_by_dataset_and_session():
    from gq.data import HAND, load_hand

    if not HAND.exists():
        return
    train, test = load_hand("train"), load_hand("test")
    assert train and test
    assert not {r["dataset"] for r in train} & {r["dataset"] for r in test}
    assert not {r["session"] for r in train} & {r["session"] for r in test}


def test_batch2_test_set_shares_no_owner_with_dev():
    from gq.data import HAND2, load_hand_dev, load_hand_test

    if not HAND2.exists():
        return
    dev, test = load_hand_dev(), load_hand_test()
    assert test and dev
    owners = lambda rs: {r["dataset"].split("/")[0] for r in rs}  # noqa: E731
    assert not owners(dev) & owners(test)
    assert not {r["session"] for r in dev} & {r["session"] for r in test}
    assert not {r["text"][-300:] for r in dev} & {r["text"][-300:] for r in test}


def test_llm_labeled_data_shares_nothing_with_test_set():
    from gq.data import HAND2, load_hand_test, load_silver

    if not HAND2.exists():
        return
    extra = load_silver("silver/[0-9]*/labeled.jsonl") + load_silver("silver/pairs-*/labeled.jsonl")
    if not extra:
        return
    test = load_hand_test()
    owners = lambda rs: {r["dataset"].split("/")[0] for r in rs}  # noqa: E731
    assert not owners(extra) & owners(test)
    assert not {r["session"] for r in extra} & {r["session"] for r in test}
    assert not {r["text"][-300:] for r in extra} & {r["text"][-300:] for r in test}
    assert len({r["id"] for r in extra}) == len(extra)


def test_batch4_test_set_shares_nothing_with_other_data():
    import json

    from gq.data import ROOT, load_hand_dev, load_hand_test, load_hand_test4, load_silver

    test4 = load_hand_test4()
    if not test4:
        return
    other = load_hand_dev() + load_hand_test() + load_silver("silver/[0-9]*/labeled.jsonl")
    excluded = set(json.loads((ROOT / "data/batch4/excluded_owners.json").read_text()))
    owners = {r["dataset"].split("/")[0] for r in test4}
    assert not owners & excluded
    assert not owners & {r["dataset"].split("/")[0] for r in other}
    assert not {r["session"] for r in test4} & {r["session"] for r in other}
    assert not {r["text"][-300:] for r in test4} & {r["text"][-300:] for r in other}


def test_generator_spans_align_with_text():
    sources = {
        "gold": [{"question": "Context here. How should we ship it?", "options": ["Squash (Recommended)", "Rebase"]}],
        "eot": [],
        "carriers": ["All tests pass.\n\n- one\n- two"],
    }
    gen = Generator(sources, random.Random(0))
    for _ in range(50):
        s = gen.gold()
        for start, end, kind in s.spans:
            assert 0 <= start < end <= len(s.text)
            assert s.text[start:end].strip() == s.text[start:end]


def test_hand_augment_keeps_spans_aligned():
    text = "Earlier work.\n\nMore notes here.\n\nWant me to fix it now, or leave it for later?"
    q0 = text.index("Want")
    a0, b0 = text.index("fix it now"), text.index("leave it for later")
    spans = [(q0, len(text), "Q"), (a0, a0 + 10, "OPT"), (b0, b0 + 18, "OPT")]
    sources = {"gold": [{"question": "Ok?", "options": ["Squash", "Rebase"]}], "eot": [],
               "carriers": ["All tests pass.\n\nThe build is green now."]}
    gen = Generator(sources, random.Random(0))
    changed = 0
    for _ in range(60):
        s = gen.augment_hand(Sample(text, spans, "x"))
        changed += s.text != text
        q, *opts = s.spans
        assert s.text[q[0]:q[1]].startswith("Want me to") and s.text[q[1] - 1] == "?"
        assert all(q[0] < a < b < q[1] for a, b, _ in opts)
        assert all(s.text[a:b].strip() == s.text[a:b] for a, b, _ in opts)
    assert changed


def _compile_with(text, q_text, opt_texts):
    tokens = tokenize(text)
    labels = [LABEL_ID["O"]] * len(tokens)
    qa = text.index(q_text)
    spans = [(qa, qa + len(q_text), "Q")] + [(text.index(o), text.index(o) + len(o), "OPT") for o in opt_texts]
    for a, b, kind in spans:
        inside = [i for i, t in enumerate(tokens) if a <= t.start and t.end <= b]
        for n, i in enumerate(inside):
            if kind == "Q" and labels[i] != LABEL_ID["O"]:
                continue
            labels[i] = LABEL_ID[f"{kind}_{'B' if n == 0 else 'I'}"]
    return compile_questions(text, tokens, labels)


def test_compile_requires_question_mark():
    assert _compile_with("Restart pi and give it a try!", "Restart pi and give it a try!", []) == []


def test_compile_option_rules():
    [q] = _compile_with("Want me to fix it, or something else?", "Want me to fix it, or something else?",
                        ["fix it", "something else"])
    assert (q.kind, q.options) == ("yes_no", [])
    [q] = _compile_with("Should I fix it now, or wait for CI?", "Should I fix it now, or wait for CI?", ["fix it now"])
    assert (q.kind, q.options) == ("either_or", ["fix it now", "wait for CI"])
    [q] = _compile_with("Which package: `ai`, `tui`, `pods`, or `web`?", "Which package: `ai`, `tui`, `pods`, or `web`?",
                        ["`ai`, `tui`, `pods`, or `web`"])
    assert (q.kind, q.options) == ("multi_choice", ["ai", "tui", "pods", "web"])
    [q] = _compile_with("Could you share the error log?", "Could you share the error log?", [])
    assert q.kind == "open"


def test_compile_merges_offer_list_of_questions():
    text = "Done.\n\nWould you like me to:\n1. Add tests?\n2. Ship it now?\n3. Stop here?"
    tokens = tokenize(text)
    labels = [LABEL_ID["O"]] * len(tokens)
    for item in ("Add tests?", "Ship it now?", "Stop here?"):
        a = text.index(item)
        inside = [i for i, t in enumerate(tokens) if a <= t.start and t.end <= a + len(item)]
        labels[inside[0]] = LABEL_ID["Q_B"]
        for i in inside[1:]:
            labels[i] = LABEL_ID["Q_I"]
    [q] = compile_questions(text, tokens, labels)
    assert (q.kind, q.propose, q.options) == ("multi_choice", True, ["Add tests", "Ship it now", "Stop here"])


def test_hand_sets_group_by_last_question():
    from gq.evaluate import hand_agreement, hand_sets

    text = "Done. Want me to push?"
    q = {"kind": "yes_no", "propose": True, "prompt": "Want me to push?", "options": [], "default": None,
         "multiSelect": False}
    rows = [{"id": "a", "text": text, "spans": [[6, 22, "Q", "Want me to push?"]], "expected": [q]},
            {"id": "b", "text": "All done.", "spans": [], "expected": []}]
    sets, expected = hand_sets(records=rows)
    assert [s.source for s in sets["hand/all"]] == ["a", "b"]
    assert [s.source for s in sets["hand/yes_no"]] == ["a"]
    assert [s.source for s in sets["hand/negative"]] == ["b"]
    assert sets["hand/all"][0].spans == [(6, 22, "Q")]
    got = hand_agreement(sets["hand/all"], expected, [[dict(q)], []])
    assert got["kind_acc"] == 1.0 and got["propose_acc"] == 1.0
