# 19 Discussion Round Handler

## Goal

Drive the **post-submission discussion period**: ingest reviewer (and AC) follow-up replies, track how each reviewer's stance and score move across rounds, decide per thread whether to respond / concede / hold / escalate / stop, and draft concise follow-ups that add only new information instead of re-pasting the first-round rebuttal.

This capability turns the skill from a one-shot rebuttal into a multi-round assistant. It runs after the first rebuttal is submitted (11 → 14 passed) and reruns each time new reviewer activity appears, until the discussion window closes.

## Where this runs in the lifecycle

- Precondition: a first-round response was drafted (11), passed the safety gate (14), and was submitted.
- Trigger: a reviewer or AC posts a reply, asks a follow-up, signals a score change, or the user pastes new discussion activity.
- Loop: ingest → classify → decide per thread → draft deltas → safety gate (14) → submit → update engagement → wait for next activity.
- Exit: discussion window closes, or every decision-relevant thread is resolved/stopped.

## Relationship to 18, 05, and 14

| | This capability (19) | Related |
|---|---|---|
| Pre-built answers | Consumes `rehearsal_memory.anticipated_followups` from **18** as a ready answer bank | 18 |
| Ingesting raw replies | Reuses the normalization/anchor pattern from **05** for follow-up text | 05 |
| New concern in a reply | Routes back to 06 → 10 → 08 for fresh analysis/experiment/strategy | 06/10/08 |
| Posting anything | Every drafted follow-up must pass **14** before it is posted | 14 |

19 does not invent reviewer positions and does not approve text for posting; 14 remains the gate.

## Language policy

Discuss thread decisions with the user in the user's language. Posted follow-up prose follows `project_memory.language_policy` (English by default unless venue rules permit otherwise). Preserve exact reviewer wording, metric names, and IDs.

## Required inputs

Read before handling a round:

- `.awesome-rebuttal/memory/discussion_memory.json` — this capability's own state across rounds (create on first run)
- `.awesome-rebuttal/memory/response_memory.json` from 11 — what was already said in round 1 (so follow-ups add deltas only)
- `.awesome-rebuttal/memory/rehearsal_memory.json` from 18, if present — the anticipated follow-up answer bank
- `.awesome-rebuttal/memory/review_memory.json` from 05 — original reviews, stable labels, anonymous IDs, initial scores/confidence
- `.awesome-rebuttal/memory/review_analysis_memory.json` from 06 — semantic concern cards to map follow-ups onto
- `.awesome-rebuttal/memory/strategy_memory.json` from 08 — stances and coverage plan
- `.awesome-rebuttal/memory/experiment_memory.json` from 10 — for newly completed `EXP-*` results a follow-up can now report
- `.awesome-rebuttal/memory/paper_memory.json` / `code_memory.json` — evidence anchors
- confirmed venue rules — discussion-period permissions: follow-up allowed? per-reviewer vs global? nudging allowed? deadline?

The reviewer's new reply text is user-provided (pasted) or read from a file the user points to. Do not assume a reviewer's position if they have not actually replied.

## Outputs

```text
.awesome-rebuttal/
├── memory/discussion_memory.json
├── drafts/discussion_round_<n>_followups.md
├── drafts/reviewer_engagement.md      # rendered human-readable tracker
└── logs/discussion_round_<n>_report.md
```

Store anchors and short summaries of reviewer replies; do not copy long private discussion threads verbatim into persisted memory beyond what is needed for traceability.

## Boundary

### This capability does

- ingest and normalize reviewer/AC follow-up replies per round
- classify each reply (resolved, still unconvinced, new question, score signal, procedural, AC question, off-topic)
- maintain a reviewer engagement tracker: initial vs current score, delta, reply state, open/resolved concerns, next action
- decide per thread: respond / concede / hold / escalate to AC / stop
- draft concise, delta-only follow-ups using the 18 answer bank and any newly available evidence
- detect and route genuinely new concerns back to 06/10/08
- assess diminishing returns and recommend when to stop
- enforce discussion etiquette (no badgering, no score demands)

### This capability does not

- fabricate reviewer replies, positions, or score changes
- assume silence means agreement or disagreement
- re-paste the first-round rebuttal as a "follow-up"
- nudge or pressure reviewers for a score change
- post anything without passing 14
- record a score as final unless the reviewer/AC actually stated it (mark inferred vs stated)

## Round model

Discussion is multi-round. Keep an explicit counter and per-round record.

```json
{
  "current_round": 2,
  "discussion_window": {
    "opens": "2026-06-10T00:00:00+08:00",
    "closes": "2026-06-17T23:59:00+08:00",
    "timezone": "Asia/Shanghai",
    "venue_allows_followup": "yes|no|limited|unknown",
    "followup_scope": "per_reviewer|global|both|unknown",
    "nudge_policy": "allowed_once|discouraged|forbidden|unknown"
  },
  "rounds": [
    {"round_id": "round-1", "kind": "initial_rebuttal", "submitted_at": "...", "summary": "First rebuttal submitted."},
    {"round_id": "round-2", "kind": "discussion_followup", "submitted_at": null, "summary": "Reviewer replies received; drafting deltas."}
  ]
}
```

`round-1` is the initial rebuttal (owned by 11). Round 2+ are discussion follow-ups owned by this capability.

## Ingesting follow-up replies

Reuse 05's normalization discipline. For each incoming reply build a record:

```json
{
  "followup_id": "FU-R2-r2-01",
  "round_id": "round-2",
  "reviewer": {"stable_label": "R2", "anonymous_id": "<id_or_unknown>", "is_ac": false},
  "raw_excerpt_anchor": "discussion_memory:R2.round2.raw",
  "classification": "acknowledged_resolved|still_unconvinced|partial|new_question|score_signal|procedural|ac_question|off_topic",
  "refers_to_concern_ids": ["SC003"],
  "refers_to_response_unit_ids": ["RU-004"],
  "is_new_concern": false,
  "score_signal": {"type": "raised|lowered|will_consider|none", "stated_value": "<value_or_unknown>", "source": "stated|inferred"},
  "sentiment": "positive|neutral|negative|mixed",
  "requires_response": "yes|optional|no",
  "priority": "decision_critical|high|medium|low"
}
```

Rules:

- Map each reply to existing concern IDs and the round-1 response unit it follows up on.
- `score_signal.source` must be `stated` only when the reviewer explicitly stated a number/direction; otherwise `inferred` and treated as a hypothesis.
- If `is_new_concern: true`, flag it for routing to 06/10/08; do not improvise a deep answer inside the discussion handler.

## Reviewer engagement tracker

Maintain one row per reviewer (and AC), updated every round. This is the lightweight score/engagement dashboard.

```json
{
  "stable_label": "R2",
  "anonymous_id": "<id_or_unknown>",
  "initial_score": "4",
  "initial_confidence": "4",
  "current_score": "4",
  "score_delta": "0",
  "score_source": "stated|inferred|unchanged_assumed",
  "replied_in_discussion": "yes|no|unknown",
  "last_reply_round": "round-2",
  "stance_now": "satisfied|still_unconvinced|new_question|silent|disengaged",
  "open_concern_ids": ["SC003"],
  "resolved_concern_ids": ["SC001", "SC007"],
  "next_action": "respond|concede|hold|escalate_ac|stop",
  "etiquette_note": "Replied once and is satisfied; do not nudge."
}
```

Render `reviewer_engagement.md` as a newest-state table so the user can see at a glance who moved, who is silent, and where the remaining battle is. Never write an `inferred` score as if it were `stated`.

## Per-thread decision model

For each reviewer/AC thread, choose one decision:

- `respond` — there is a concrete, new, decision-relevant thing to say.
- `concede` — the reviewer is right on a bounded point; acknowledge narrowly without collapsing the core claim.
- `hold` — wait for another reviewer/AC, a pending result, or a user decision before replying.
- `escalate_ac` — the decision-relevant fact belongs in an AC-facing message (route framing through 13's posture and 14's gate; only if rules allow AC/global discussion text).
- `stop` — further replies add no value or risk badgering; close the thread politely if a closing is warranted.

```json
{
  "thread_id": "R2-r2",
  "reviewer": {"stable_label": "R2", "anonymous_id": "<id_or_unknown>"},
  "decision": "respond",
  "rationale": "R2 still doubts the baseline; EXP-004 is now complete and directly answers it.",
  "uses_anticipated_bank": ["anticipated_followups:why-not-compare-method-X"],
  "needs_new_evidence": "EXP-004|none",
  "draft_followup_id": "DF-R2-r2",
  "length_target": "short",
  "must_avoid": ["repeating round-1 text", "asking for a score raise"],
  "user_decision_required": false
}
```

## Drafting discipline: delta-only, no repetition

A follow-up is not a second rebuttal. Each drafted follow-up must:

1. **Reference, not repeat** — point to the round-1 response unit ("As noted in our response to your Q2, ...") and add only what is new.
2. **Lead with the new fact** — a newly completed result, a precise clarification, or a bounded concession.
3. **Stay short** — a few sentences; discussion replies are read quickly.
4. **Answer the actual follow-up**, in the reviewer's terms, not a restatement of the original answer.
5. **Close threads cleanly** — when a reviewer is satisfied, one brief thanks; do not re-argue.

Use the 18 answer bank: if an `anticipated_followups` entry matches the incoming question, adapt its `draft_short_answer` (verify its evidence anchor is still valid and any `needs_result` is now satisfied) rather than writing from scratch.

New approved experiment results may be reported here only when `experiment_memory.result_status` is `already_done`/verified and venue rules allow new results in discussion — same discipline as 11.

## Score-signal and etiquette handling

Discussion rounds have a specific failure mode: pestering reviewers. Enforce etiquette:

- Never ask a reviewer to raise their score. State evidence; let them decide.
- Do not post repeated nudges. If a reviewer is silent and the venue `nudge_policy` is `allowed_once`, a single short, polite pointer is permitted **only with user approval**; if `discouraged`/`forbidden`, do not nudge.
- Do not imply other reviewers' positions to pressure one reviewer.
- If a reviewer lowered their score after the rebuttal, respond with calm, factual clarification, not defensiveness; check whether a round-1 statement caused it (route to 18 to diagnose if useful).
- Treat `inferred` score movement as a working hypothesis for prioritization only, never as a claim in posted text.

## When to stop / diminishing returns

Recommend `stop` for a thread when any holds:

- the reviewer explicitly stated satisfaction or raised the score → one brief thanks, then stop;
- two exchanges produced no movement and no new information is available → a further reply likely irritates;
- the reviewer is silent and nudging is discouraged/forbidden → stop;
- the remaining gap requires evidence that cannot be produced before the deadline → state the bounded future-work framing once, then stop;
- the deadline is near → reallocate effort to decision-critical threads.

Record a `stop_assessment` summarizing which threads are closed, which remain active, and why.

## Routing new concerns

If a follow-up raises a genuinely new concern (`is_new_concern: true`):

- route to `06_situation_analyzer.md` to interpret it,
- route to `10_experiment_triage.md` if it implies new evidence,
- route to `08_strategy_planner.md` if it changes the plan,
- then return here to draft the follow-up.

Do not answer a substantive new concern off-the-cuff inside the discussion handler.

## Questionnaire protocol

Use `references/core/user_questionnaire_protocol.md` when:

- venue discussion permissions (follow-up scope, nudging, deadline) are unconfirmed;
- a reviewer is silent and the user must decide whether to send one allowed nudge;
- a follow-up depends on a result the user must confirm is complete;
- a thread needs a choice between conceding and pushing once more;
- escalating a fact to the AC is sensitive.

Recommended questionnaire shape:

```json
{
  "questionnaire_id": "discussion_round_v1",
  "summary_before_question": "Round 2: R2 still wants the baseline (EXP-004 is now done and answers it), R3 is satisfied and raised to 6, R1 is silent. I recommend responding to R2, thanking R3 briefly, and not nudging R1.",
  "questions": [
    {"id": "respond_scope", "type": "multi_select", "prompt": "Which threads should I draft follow-ups for?", "options": ["R2_respond", "R3_thanks_close", "R1_no_action", "R1_one_polite_nudge_if_allowed"]},
    {"id": "report_new_result", "type": "single_choice", "prompt": "May I report EXP-004's completed result to R2?", "options": ["yes_verified", "not_yet_confirmed", "do_not_report"]},
    {"id": "stop_or_continue", "type": "single_choice", "prompt": "After this round, what is the default stance?", "options": ["stop_when_threads_resolved", "keep_pushing_low_score", "minimize_risk_until_deadline"]}
  ]
}
```

## Output schema sketch

```json
{
  "version": "0.1",
  "status": "active|closed|blocked",
  "discussion_window": {},
  "current_round": 2,
  "rounds": [],
  "reviewer_engagement": [],
  "incoming_followups": [],
  "thread_decisions": [],
  "drafted_followups": [],
  "new_concerns_routed": [],
  "anticipated_bank_usage": [],
  "stop_assessment": {},
  "etiquette_flags": [],
  "routes": [],
  "open_questions": []
}
```

## Output report

```markdown
## Discussion Round 2

- Status: active|closed|blocked
- Window closes: 2026-06-17 (4 days left)
- Venue: per-reviewer follow-up allowed; nudging discouraged

### Reviewer engagement
| Reviewer | Initial | Current | Delta | Replied | Stance | Next action |
|---|---|---|---|---|---|---|
| R1 | 3 | 3 (assumed) | 0 | no | silent | hold / no nudge |
| R2 | 4 | 4 (stated) | 0 | yes | still_unconvinced | respond (EXP-004) |
| R3 | 5 | 6 (stated) | +1 | yes | satisfied | thanks + close |

### Drafted follow-ups (delta-only)
- DF-R2-r2 — reports completed EXP-004; references round-1 Q2; ~3 sentences.
- DF-R3-r2 — one-line thanks; closes thread.

### New concerns routed
- (none) / FU-R2-r2-02 → 06 then 10

### Stop assessment
- Close: R3. Active: R2. Hold: R1 (no nudge per venue).

### Routes
- 14_safety_rule_checker.md — before posting any follow-up
- 06/10/08 — only if a new concern appears
```

## Procedure

1. **Load state** — read or create `discussion_memory.json`; load round-1 response, rehearsal bank, review/analysis/strategy/experiment memory, and venue discussion rules.
2. **Confirm permissions** — follow-up scope, nudging policy, deadline; ask if unconfirmed.
3. **Ingest replies** — normalize each reviewer/AC reply into a follow-up record with anchors and classification.
4. **Update engagement tracker** — set current score (stated vs inferred), stance, open/resolved concerns per reviewer.
5. **Decide per thread** — respond / concede / hold / escalate_ac / stop, with rationale.
6. **Route new concerns** — send genuinely new concerns to 06/10/08 before drafting.
7. **Draft delta-only follow-ups** — reuse the 18 answer bank; verify evidence; keep short; reference round-1 instead of repeating.
8. **Etiquette check** — no score demands, no disallowed nudges, no reviewer-vs-reviewer pressure.
9. **Stop assessment** — mark closed/active/hold threads and diminishing-returns reasoning.
10. **Persist + render** — write `discussion_memory.json`, follow-up drafts, the engagement table, and the round report.
11. **Route to 14** — every follow-up passes the safety gate before posting; snapshot via 09 at the end of the round.

## Stop / proceed rules

Proceed to draft follow-ups when:

- incoming replies are classified and mapped to concerns/response units,
- the engagement tracker distinguishes stated vs inferred scores,
- venue follow-up permissions are known,
- evidence for any new claim is verified or marked needs_user_input.

Proceed with warning when:

- some reviewers are silent (do not infer their stance),
- a result is "expected soon" but not yet verified (do not report it as done),
- venue nudging policy is unconfirmed (default to no nudge).

Stop and ask when:

- venue rules may forbid follow-up or the deadline is unclear,
- a reply raises a substantive new concern needing 06/10/08,
- a follow-up would depend on an unverified result,
- a silent reviewer tempts a nudge that rules discourage,
- escalating to the AC is sensitive and needs user approval.

## Safety rules

- Never fabricate reviewer replies, positions, or score changes; mark inferred vs stated.
- Never treat silence as agreement or as license to nudge.
- Never ask a reviewer to raise a score or pressure them with other reviewers' views.
- Never re-paste the first-round rebuttal as a follow-up; add deltas only.
- Report new results only when verified and rule-allowed, same as 11.
- Every posted follow-up must pass `14_safety_rule_checker.md`.
- Respect anonymity/privacy and the venue's discussion-period rules at all times.
