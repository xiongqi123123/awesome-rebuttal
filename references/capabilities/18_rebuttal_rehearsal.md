# 18 Rebuttal Rehearsal

## Goal

Stress-test a drafted rebuttal **before** the final safety gate by simulating how reviewers and the AC will read it against the paper. The output is a set of predicted reactions, residual doubts, likely follow-up questions, and concrete hardening suggestions that route back to `11_response_writer.md` (and `13_ac_summary_writer.md`).

Run this after a response draft exists (11), and after an AC summary draft if one is planned (13), but before `14_safety_rule_checker.md`. Rehearsal improves persuasiveness; the safety checker enforces rules. They are different jobs.

## Relationship to the safety checker (14)

These two capabilities must not be merged or confused:

| | 18 Rehearsal | 14 Safety checker |
|---|---|---|
| Question | "Will this convince the reviewer/AC?" | "Is this allowed, sourced, and non-hostile?" |
| Method | Simulate reviewer/AC personas reading paper + rebuttal | Audit claims against memory and venue rules |
| Output | Predicted reactions, weaknesses, follow-ups, hardening list | Gate verdicts (pass/blocked/needs_user_confirmation) |
| Can block submission? | No — advisory; it recommends edits | Yes — it is the final gate |

Rehearsal never grants submission approval. After hardening, the draft must still pass 14.

## Language policy

Discuss rehearsal findings with the user in the user's language. Persona simulations should read and reason in the language of the paper/reviews/draft. Any rebuttal-prose edits suggested for the draft follow the submission-language policy in `project_memory.language_policy` (English by default).

## Required inputs

Read before rehearsing:

- `.awesome-rebuttal/memory/response_memory.json` from 11 — required (the draft to test)
- `.awesome-rebuttal/drafts/author_response_draft.md` (and per-reviewer/PDF drafts) — required
- `.awesome-rebuttal/memory/review_memory.json` from 05 — required for raw reviews, stable labels, anonymous IDs, scores/confidence
- `.awesome-rebuttal/memory/review_analysis_memory.json` from 06 — required for semantic concern cards and common clusters
- `.awesome-rebuttal/memory/paper_memory.json` from 03 — required for the materials each persona reads
- `.awesome-rebuttal/memory/code_memory.json` from 04 — required when the draft relies on implementation/results
- `.awesome-rebuttal/memory/strategy_memory.json` from 08 — read by the **orchestrator only**, never given to persona subagents
- `.awesome-rebuttal/memory/experiment_memory.json` from 10 — for result-status checks during aggregation
- `.awesome-rebuttal/memory/ac_summary_memory.json` from 13, if present
- confirmed venue rules — for what a real follow-up round would even allow

If the response draft is missing, route back to 11. If paper memory is missing, rehearsal can run in a degraded mode but must mark paper-grounding as `unverified` and warn that persona reactions are low-confidence.

## Outputs

Write skill-owned outputs under the active workspace:

```text
.awesome-rebuttal/
├── memory/rehearsal_memory.json
├── drafts/rehearsal_findings.md
├── drafts/hardening_todo.md
└── logs/rehearsal_report.md
```

Persona transcripts may be stored under `.awesome-rebuttal/cache/rehearsal/<persona_id>.md` as disposable evidence. Do not copy raw full paper text or private code into persisted memory; store anchors and summaries.

## Boundary

### This capability does

- reconstruct reviewer personas from `review_memory` / `review_analysis_memory`
- run one or more **isolated** persona evaluations of paper-vs-rebuttal
- predict per-concern reactions: resolved / partially / unresolved, with reasons
- collect residual doubts and likely discussion-round follow-up questions
- estimate (and clearly label as simulated) possible score movement and meta-review framing
- detect rebuttal-introduced problems: over-claims, self-contradiction, dodged concerns, concessions that leak into unrelated claims
- aggregate persona findings into a prioritized hardening list for 11/13
- prime `19_discussion_round_handler.md` with a pre-built follow-up answer bank

### This capability does not

- approve text for submission (that is 14)
- invent new paper facts, experiment results, or real reviewer positions
- write final rebuttal prose (it recommends edits; 11 applies them)
- record simulated scores as real reviewer scores anywhere in `review_memory`
- leak strategy intent into persona subagents
- send private workspace content to an external service without user awareness (see Safety rules)

## Subagent orchestration

Rehearsal is defined in terms of **persona evaluations**. How they execute depends on host capability.

### Execution modes

- **Isolated-subagent mode (preferred when the host supports it):** spawn one independent agent per persona. Each agent starts cold with only its persona prompt and the materials that persona is allowed to see. Agents do not share context with each other or with the orchestrator's strategy reasoning. Run them in parallel when the host allows.
- **In-context fallback mode:** if the host has no subagent/parallel-agent API, run each persona as a separate, clearly delimited role-play pass in the main context. Before each pass, explicitly "forget" strategy framing and read only the allowed materials. The output schema is identical to isolated mode.

Record the chosen mode in `rehearsal_memory.execution_mode`.

### Isolation contract (mandatory in both modes)

A persona must only receive:

1. the paper (or `paper_memory` digest + key anchors),
2. the rebuttal text it is meant to react to,
3. for a **reconstructed** reviewer: that reviewer's original review and scores,
4. its persona instructions.

A persona must **never** receive: `strategy_memory`, the selected strategy lens, the skill's goals, the hardening list, other personas' outputs, or any hint of the "intended" answer. Contaminating a persona defeats the purpose — it will rubber-stamp the draft.

### Privacy contract

Persona subagents operate on workspace materials only. If the host runs subagents in the cloud or sends content to an external API, treat the paper/review/draft as sensitive: confirm with the user before any external dispatch, and never include local paths, author identity, or private repository URLs in persona inputs. This mirrors the anonymity/privacy gate in 14.

## Reviewer persona model

Build personas from evidence, not imagination.

```json
{
  "persona_id": "PR-R2",
  "persona_type": "reconstructed_reviewer|independent_reviewer|ac_meta_reviewer",
  "based_on": {"stable_label": "R2", "anonymous_id": "<id_or_unknown>"},
  "source_anchors": ["review_memory:R2.raw", "review_analysis_memory:SC003"],
  "known_stance": "low_score|borderline|supportive|unknown",
  "known_score": "<score_or_unknown>",
  "known_confidence": "<confidence_or_unknown>",
  "concern_focus": ["SC003", "SC007"],
  "materials_allowed": ["paper_memory", "R2_original_review", "rebuttal_text_for_R2"],
  "materials_forbidden": ["strategy_memory", "other_personas", "hardening_list"]
}
```

Recommended persona set:

- one `reconstructed_reviewer` per real reviewer who matters (always include every low-score/high-confidence reviewer),
- at least one `independent_reviewer` (fresh skeptical reader who never saw the original reviews — catches blind spots shared by the original panel and over-claims the rebuttal newly introduces),
- one `ac_meta_reviewer` when the venue has a meta-review/AC decision and an AC summary is planned.

Keep the set small and decision-relevant; do not simulate minor reviewers in depth if space and time are limited.

## Persona prompt templates

Paste-ready prompts for each persona subagent. Fill the `<...>` slots from memory. Keep each persona in character and force structured output so aggregation is mechanical.

### Template A — Reconstructed reviewer

```text
You are Reviewer <stable_label> for a <venue/field> submission. You wrote the original
review below. You have NOT seen the authors' internal strategy and you do NOT know what
answer they are hoping for. Stay strictly in character as this reviewer.

PAPER (claims, scope, evidence):
<paper_memory digest + key table/section anchors, or paper excerpt>

YOUR ORIGINAL REVIEW (your concerns, your score, your confidence):
<raw review text + score/confidence>

THE AUTHORS' REBUTTAL ADDRESSED TO YOU:
<per-reviewer reply, or the unified/global sections relevant to your concerns>

Re-read your concerns one by one and react honestly as this reviewer:
- For each original concern: is it RESOLVED, PARTIALLY resolved, or UNRESOLVED, and why?
- What residual doubts remain after this rebuttal?
- What follow-up question(s) would you actually post in the discussion period?
- Does anything in the rebuttal newly worry you (over-claim, inconsistency with the paper,
  a dodged question, or a concession that weakens their main claim)?
- Would you change your score? From what, to what, and what exactly would have to be true
  for you to raise it? (This is a SIMULATED estimate of your own likely behavior.)

Ground every reaction in the paper or the rebuttal text provided. Do not invent facts about
the paper that are not shown to you. Output ONLY this JSON:
{
  "persona_id": "PR-<label>",
  "per_concern": [{"concern_id": "...", "verdict": "resolved|partial|unresolved", "why": "..."}],
  "residual_doubts": ["..."],
  "followup_questions": ["..."],
  "rebuttal_introduced_risks": ["..."],
  "predicted_score_movement": {"from": "...", "to": "...", "direction": "up|none|down", "conditions": "...", "confidence": "low|medium|high"},
  "overall_reaction": "convinced|partially_convinced|unconvinced",
  "one_line_summary": "..."
}
```

### Template B — Independent reviewer (fresh skeptical reader)

```text
You are an independent, competent, skeptical reviewer in <field>. You did NOT write any of
the original reviews and you have NOT seen them. You are reading this paper and its rebuttal
fresh, the way a newly assigned reviewer or a careful AC would. You do not know the authors'
strategy or desired outcome.

PAPER (claims, scope, evidence):
<paper_memory digest + key anchors, or paper excerpt>

THE AUTHORS' REBUTTAL:
<full rebuttal text / one-page draft / global comment>

Evaluate as a fresh expert:
- Which claims in the rebuttal are NOT fully supported by the paper or by stated evidence?
- Where does the rebuttal concede something that quietly undermines the paper's main claim?
- What questions would a careful reader still have that the original reviewers may have missed?
- Does the rebuttal read as evidence-backed, or hand-wavy / argumentative / apologetic?
- Are there internal inconsistencies (different numbers, scope, or framing in different places)?
- Your overall lean: lean_accept | borderline | lean_reject, with reasons.

Do not assume facts not shown to you. Output ONLY this JSON:
{
  "persona_id": "PR-INDEP",
  "unsupported_claims": ["..."],
  "self_undermining_concessions": ["..."],
  "open_questions_panel_missed": ["..."],
  "tone_assessment": "evidence_backed|mixed|hand_wavy",
  "internal_inconsistencies": ["..."],
  "overall_lean": "lean_accept|borderline|lean_reject",
  "one_line_summary": "..."
}
```

### Template C — AC / meta-reviewer

```text
You are the Area Chair / meta-reviewer who must write the decision summary for this paper.
You see the review record and the authors' rebuttal. You do not see the authors' internal
strategy. Be neutral and decision-focused; do not pit reviewers against each other.

REVIEW RECORD (concerns, scores/confidence if available):
<review_memory digest: per-reviewer concerns + scores>

THE AUTHORS' REBUTTAL (and AC summary, if any):
<global/AC-facing text + key per-reviewer deltas>

As the AC:
- Which decision-relevant facts actually land from this rebuttal?
- Does the rebuttal change the picture for the lowest-score concern? How?
- Which single unresolved concern would most justify a reject if left unaddressed?
- How would you frame the meta-review after reading this rebuttal?
- What would have to be true for you to lean accept?

Output ONLY this JSON:
{
  "persona_id": "PR-AC",
  "landed_facts": ["..."],
  "lowest_score_concern_status": "addressed|partially|not_addressed",
  "most_decisive_unresolved_concern": "...",
  "predicted_meta_review_framing": "...",
  "tip_to_accept_conditions": ["..."],
  "one_line_summary": "..."
}
```

## Aggregation model

The orchestrator (which may see strategy_memory) merges persona JSON into findings. Cross-check each persona claim against `experiment_memory` and `paper_memory` before trusting it — a persona can misread, and a persona's "unsupported claim" flag might itself be wrong.

```json
{
  "finding_id": "RF-001",
  "type": "unresolved_concern|residual_doubt|unsupported_claim|self_contradiction|dodged_question|likely_followup|score_risk",
  "raised_by": ["PR-R2", "PR-INDEP"],
  "linked_response_unit_ids": ["RU-004"],
  "linked_concern_ids": ["SC003"],
  "severity": "decision_critical|high|medium|low",
  "orchestrator_check": "confirmed|persona_misread|needs_user_input",
  "evidence_anchor": "paper_memory:table_2|experiment_memory:EXP-001|none",
  "recommended_fix": "Add the verified Table 2 value to RU-004; soften 'significantly' to 'consistently'.",
  "fix_owner": "11_response_writer|13_ac_summary_writer|user|not_fixable_now",
  "feeds_discussion_round": true
}
```

Rank findings by how many personas raised them and by severity; concerns flagged by both a reconstructed reviewer and the independent reviewer are the highest-value fixes.

## Predicted score movement policy

- Predicted scores are **simulations**, labeled `predicted_*` and `confidence`.
- Never write a simulated score into `review_memory` or present persona text as a real reviewer's words.
- Use predicted movement only to prioritize hardening, never as a claim in the rebuttal ("this will raise the score" is prohibited by 14's tone gate anyway).
- If personas disagree sharply, record the spread rather than averaging into false precision.

## Hardening handoff

Write `.awesome-rebuttal/drafts/hardening_todo.md` as an ordered, actionable list for 11/13:

- each item = finding ID, target response unit, the exact weakness, and the concrete edit;
- separate "must fix before submitting" (decision_critical / high) from "optional polish";
- mark items that need a user decision or a missing number as `needs_user_input`;
- carry `feeds_discussion_round: true` items into the follow-up answer bank for 19.

## Follow-up answer bank (primes 19)

Likely follow-up questions collected from personas become a pre-drafted bank so the discussion round is fast:

```json
{
  "anticipated_followups": [
    {"question": "Why not compare against <method X>?", "raised_by": ["PR-R2"], "draft_short_answer": "", "evidence_anchor": "EXP-004", "status": "drafted|needs_result|needs_user_input"}
  ]
}
```

Do not paste these into the first-round rebuttal; hold them for `19_discussion_round_handler.md`.

## Questionnaire protocol

Use `references/core/user_questionnaire_protocol.md` when:

- the host supports subagents and the user must approve spawning them (or external dispatch on a cloud host);
- the user must choose which personas to simulate under time limits;
- a rehearsal finding requires a user decision (e.g., run a missing experiment vs. soften a claim);
- personas disagree on whether a concern is resolved and the fix changes strategy.

Recommended questionnaire shape:

```json
{
  "questionnaire_id": "rehearsal_setup_v1",
  "summary_before_question": "I can rehearse the draft by simulating R1 (low score), R3 (borderline), one fresh independent reviewer, and the AC. R1 and R3 are the highest-value.",
  "questions": [
    {"id": "persona_scope", "type": "multi_select", "prompt": "Which personas should I simulate?", "options": ["reconstruct_all_reviewers", "reconstruct_low_and_borderline_only", "add_independent_reviewer", "add_ac_meta_reviewer"]},
    {"id": "execution_mode", "type": "single_choice", "prompt": "How should personas run?", "options": ["isolated_subagents_if_supported", "in_context_roleplay", "decide_for_me"]},
    {"id": "external_dispatch", "type": "single_choice", "prompt": "If subagents run in the cloud, may I send the paper/draft?", "options": ["yes_ok", "local_only", "ask_again_before_sending"]}
  ]
}
```

## Output schema sketch

```json
{
  "version": "0.1",
  "status": "complete|partial|blocked",
  "execution_mode": "isolated_subagents|in_context_roleplay",
  "paper_grounding": "verified|unverified",
  "source_response_memory": ".awesome-rebuttal/memory/response_memory.json",
  "personas": [],
  "persona_outputs": [],
  "findings": [],
  "predicted_score_movement_summary": {},
  "hardening_list": [],
  "anticipated_followups": [],
  "coverage_of_findings": {"must_fix": 0, "optional": 0, "needs_user_input": 0},
  "routes": [],
  "open_questions": []
}
```

## Output report

```markdown
## Rebuttal Rehearsal

- Status: complete|partial|blocked
- Execution mode: isolated_subagents|in_context_roleplay
- Personas simulated: R1 (low), R3 (borderline), independent, AC
- Paper grounding: verified|unverified

### Predicted reactions
| Persona | Overall | Predicted score | Top residual doubt |
|---|---|---|---|
| R1 | unconvinced | 3 -> 4 (if EXP-001 reported) | Baseline still missing |
| R3 | partially | 5 -> 6 | Wants sensitivity numbers |
| Independent | borderline | n/a | "Significantly" not supported |
| AC | — | — | Novelty framing still the deciding concern |

### Highest-value hardening (must fix)
1. RF-001 (R1+Independent): add verified Table 2 value to RU-004; soften "significantly".
2. ...

### Anticipated discussion-round follow-ups (held for 19)
- ...

### Routes
- 11_response_writer.md — apply must-fix hardening
- 13_ac_summary_writer.md — if AC framing needs adjustment
- 14_safety_rule_checker.md — after hardening
```

## Procedure

1. **Validate prerequisites** — confirm a response draft (11) exists; load review, analysis, paper, code, experiment memory.
2. **Build persona set** — reconstruct reviewers from `review_memory`; add an independent reviewer and (if applicable) an AC. Always include low-score/high-confidence reviewers.
3. **Choose execution mode** — isolated subagents if the host supports them; else in-context role-play. Ask the user if external/cloud dispatch is involved.
4. **Prepare isolated inputs** — give each persona only its allowed materials; strip all strategy framing.
5. **Run personas** — collect structured JSON from each persona prompt (A/B/C).
6. **Aggregate and verify** — merge into findings; cross-check each persona claim against paper/experiment memory; mark `persona_misread` where the persona was wrong.
7. **Rank and build hardening list** — prioritize multi-persona, decision-critical findings; write `hardening_todo.md`.
8. **Build follow-up answer bank** — store anticipated follow-ups for 19; do not inject into the first-round draft.
9. **Persist** — write `rehearsal_memory.json`, findings, hardening list, and report.
10. **Route** — to 11/13 for hardening, then to 14 for the final gate.

## Stop / proceed rules

Proceed to hardening when:

- at least the low-score/high-confidence reviewers and one independent reviewer were simulated,
- findings are ranked with severity and an owner,
- simulated scores are labeled as predictions.

Proceed with warning when:

- paper grounding is `unverified` (degraded confidence),
- only a subset of personas could run under time limits,
- the host could not isolate subagents and role-play was used instead.

Stop and ask when:

- no response draft exists (route to 11),
- subagents would dispatch private content externally without user approval,
- a finding requires a user decision (run experiment vs. soften claim) before the draft can be fixed.

## Safety rules

- Persona simulations are predictions, not real reviewer positions; never record them as real scores or quote them as real reviewer statements.
- Never contaminate a persona with strategy intent or the desired answer.
- Never invent paper facts or experiment results inside a persona or in a finding.
- Rehearsal cannot approve submission; the draft must still pass `14_safety_rule_checker.md`.
- Respect anonymity/privacy: no external dispatch of sensitive workspace content without user awareness, and no author-identifying details in persona inputs.
- A persona's flag can be wrong; the orchestrator must verify each finding against memory before sending it to 11/13.
