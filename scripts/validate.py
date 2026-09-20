#!/usr/bin/env python3
"""Validate content/items.json. Exit code 1 if any error is found.

Rules (see CLAUDE.md): schema, per-tier spoiler-severity arrays, keyword spoiler
lint, MVP scope (Prologue and Act 1 only), trust-status consistency.
"""
import json, re, sys, collections

LENSES = {"powermonger", "storyline_deciders", "stylist", "platinum", "missable_content"}
STATUSES = {"unverified", "source_verified"}
MISSABLE = {"none", "soft", "permanent", "unclear"}
# term -> minimum severity its presence requires in the tier's first-milestone value
LINT = {"Axon": 2, "Monolith": 2, "Renoir": 3, "Verso": 2, "Reacher": 2, "Sirene": 1,
        "Endless Tower": 2, "White Sands": 2, "Flying Manor": 1, "Floating Cemetery": 1,
        "Serpenphare": 2, "Francois": 2, "ending": 2, "Ending": 2, "dies": 3, "death": 3,
        "Golgra": 2, "Old Lumiere": 2, "Esquie": 1, "Monoco": 1, "Sciel": 1, "Simon": 2, "Clea": 1}
# display fields that are always visible must not mention later acts
LATER_ACT = re.compile(r"\bAct\s*[23]\b|\bAct (?:two|three)\b", re.I)


def validate(d):
    errs, warn = [], []
    ms = d["_meta"]["milestones"]
    playable = d["_meta"].get("playable_milestones", ms)
    ids = collections.Counter(i["id"] for i in d["items"])
    errs += [(k, "duplicate id") for k, v in ids.items() if v > 1]
    for it in d["items"]:
        i = it["id"]
        if set(it["impact"]) != set(it["lenses"]): errs.append((i, "impact keys != lenses"))
        if not set(it["lenses"]) <= LENSES: errs.append((i, "unknown lens"))
        if any(v not in range(1, 6) for v in it["impact"].values()): errs.append((i, "impact outside 1-5"))
        if it.get("missable") not in MISSABLE: errs.append((i, "bad missable value"))
        w = it["window"]
        if w["from"] not in ms or (w["until"] not in ms and w["until"] != "unclear"):
            errs.append((i, "window uses unknown milestone"))
        elif w["until"] != "unclear" and ms.index(w["from"]) > ms.index(w["until"]):
            errs.append((i, "window from is after until"))
        if w["from"] not in playable: errs.append((i, "outside MVP scope: window starts in " + w["from"]))
        prev = None
        for t in ("t1", "t2", "t3"):
            s = it["tiers"][t]["sev"]
            if len(s) != len(ms) or not all(0 <= x <= 3 for x in s) or any(a < b for a, b in zip(s, s[1:])):
                errs.append((i, t, "severity array invalid", s))
            if prev and any(a < b for a, b in zip(s, prev)): errs.append((i, t, "severity below previous tier", s, prev))
            prev = s
            txt = it["tiers"][t]["text"]
            if LATER_ACT.search(txt) and s[0] < 1:
                errs.append((i, t, "mentions a later act but severity at first milestone is 0"))
            for term, minsev in LINT.items():
                if re.search(r"\b" + re.escape(term) + r"\b", txt) and s[0] < minsev:
                    (errs if t in ("t1", "t2") else warn).append((i, t, "term '%s' needs severity >= %d at first milestone" % (term, minsev)))
        if it["tiers"]["t3"]["sev"][-1] == 3 and not it.get("tier3_cap"):
            warn.append((i, "tier 3 is S3 at the last milestone without tier3_cap"))
        if not it["sources"]: errs.append((i, "no sources"))
        n_src = len({s["name"] for s in it["sources"]})
        if it.get("status") not in STATUSES: errs.append((i, "bad status", it.get("status")))
        if it.get("status") == "source_verified" and (n_src < 2 or it.get("conflict")):
            errs.append((i, "source_verified needs >=2 sources and no conflict"))
        if it.get("status") == "unverified" and n_src >= 2 and not it.get("conflict"):
            warn.append((i, "two agreeing sources: should be source_verified"))
        for field, val in (("window.pnr", w.get("pnr")), ("conflict", it.get("conflict")), ("title_safe", it["title_safe"])):
            if val and LATER_ACT.search(val): errs.append((i, field, "mentions a later act"))
    return errs, warn


def main(path):
    d = json.load(open(path, encoding="utf-8"))
    errs, warn = validate(d)
    print("%d items; errors: %d; warnings: %d" % (len(d["items"]), len(errs), len(warn)))
    for e in errs: print("  ERROR", *e)
    for w in warn: print("  warn ", *w)
    st = collections.Counter(i["status"] for i in d["items"])
    print("status:", dict(st))
    print("lenses:", dict(collections.Counter(l for i in d["items"] for l in i["lenses"])))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "content/items.json"))
