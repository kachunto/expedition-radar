# Expedition Radar: project context for Claude Code

A spoiler-free companion for RPG players. MVP game: Clair Obscur: Expedition 33. MVP scope: **Prologue and Act 1, covered completely** (every item, including weapons and cosmetics, that a player can obtain, miss or decide in those two acts). Act 2, Act 3, the DLC and other games come later. The owner (Kachun) is building this to learn how to build a product with AI, so explain choices briefly, keep changes small and reviewable, and never add scope from the "later" list without being asked.

## Product
- A per-player checklist with five lenses: powermonger, storyline_deciders, stylist, platinum, missable_content.
- Every item has three hint tiers: t1 nudge, t2 hint, t3 detailed. Each tier stores `sev`, an array with one spoiler severity (0 none, 1 minor, 2 moderate, 3 major plot) per milestone [prologue, act1, act2, act3].
- Each item has a per-lens impact 1 to 5 (`impact` keys must equal `lenses`).
- The player sets their story point and a spoiler tolerance; tiers above the tolerance stay locked until "Reveal anyway".
- Trust badge from `status`: `source_verified` ("Sources agree": two or more distinct guides say the same, no conflict) or `unverified`. Community badges (Community verified, Disputed, Needs recheck) arrive with the votes step and are derived from votes, never hand-set.

## Hard rules
1. Never reveal ending or late-plot content. Entries that cannot safely go to tier 3 use `tier3_cap` and say so; never fake an answer.
2. No AI at runtime. AI is used only in the content pipeline (extraction, blind spoiler audit) and as the coding assistant.
3. Publish rewritten facts only. No copied guide text, images or screenshots. Every item lists its `sources`.
4. When two spoiler labelers disagree on a tier, ship the higher severity.
5. Always-visible fields (`title_safe`, `window.pnr`, `conflict`) must not name later acts or characters. Spoiler-bearing terms are only allowed in tiers with severity high enough (see LINT in `scripts/validate.py`).
6. No free-text user content in v1. No payment code; monetization is paused.
7. Do not work around sites that block automated fetching; use another source.

## Repo layout
- `content/items.json`: the data (source of truth). `content/area-map.json`: location to act mapping used to derive labels for bulk items.
- `src/template.html`: the single-file app; `src/legal.html`: Impressum and privacy (has FILL_IN markers to fill before sharing).
- `scripts/validate.py`: schema, severity and spoiler rules. `scripts/build.py`: writes `dist/`.
- `tests/`: unit tests for the validator. CI (`.github/workflows/ci.yml`) runs tests, validation and the build.

## Commands
- `python3 scripts/validate.py`  (must pass before any content change is merged)
- `python3 -m unittest discover -s tests`
- `python3 scripts/build.py`  then open `dist/index.html`

## Working style
Small commits. Run the validator and tests after every content or code change. When unsure whether something is a spoiler, mark it more severe, not less. Keep a short note in `docs/learning-log.md` when something goes wrong or a prompt needs fixing.
