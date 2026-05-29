# 03 Paper Memory Builder

## Goal

Build a durable, evidence-grounded memory of the paper itself: what story the paper tells, what logical chain supports that story, what claims are made, what experiments and comparisons support them, and what exact domain terminology the authors use.

This is one of the most important rebuttal capabilities. A rebuttal can only be strategic if the agent remembers the paper's internal logic and evidence precisely enough to answer reviewers without inventing claims or weakening the authors' intended framing.

## Boundary

### This capability does

- parse the current paper source: PDF, LaTeX, structured summary, or author-provided text
- reconstruct the paper's narrative and core logic line
- extract contributions, claims, assumptions, limitations, and terminology
- build a table/figure/result ledger with exact metric values when available
- identify datasets, tasks, metrics, baselines, ablations, qualitative studies, and efficiency results
- create a claim-to-evidence map with paper anchors
- preserve field-specific wording and acronyms for later rebuttal writing
- record reviewer-relevant hooks: what evidence can answer which likely concern categories
- write `.awesome-rebuttal/memory/paper_memory.json`

### This capability does not

- judge reviewer stance or rebuttal posture
- decide whether new experiments are worth doing
- rewrite the paper story to be more favorable than the source supports
- infer missing experimental numbers from plots or code unless clearly marked as approximate/inference
- treat code behavior as paper evidence unless linked through `04_code_memory_builder.md`
- draft final rebuttal text

## Inputs

Read these first:

- `.awesome-rebuttal/memory/project_memory.json`
- `.awesome-rebuttal/memory/source_manifest.json`
- `.awesome-rebuttal/logs/missing_information_report.md`
- paper sources under the mapped paper path, usually `Paper/`
- user-provided title/abstract/summary if no full paper is available

Acceptable paper source types:

| Source type | Use | Confidence default |
|---|---|---|
| full PDF | extract title, abstract, sections, tables, figures, references when possible | high if text/tables readable |
| LaTeX source | preferred when available; preserves labels, tables, captions, macros | high |
| PDF + LaTeX | use LaTeX for exact tables/labels, PDF for rendered structure | high |
| author summary only | use as temporary memory, mark incomplete | medium/low |
| no paper source | stop and ask; create blocked report only | none |

If multiple paper versions exist, do not choose silently. Prefer user-confirmed current submission, then newest clearly named submission artifact, then ask a version-selection questionnaire.

## Core memory model

Create paper memory around these objects.

### 1. Paper identity

Record:

- title
- short name / project alias
- venue/year if known
- field/subfield
- task setting
- paper source paths
- source version confidence
- anonymization-sensitive details, if any

### 2. Storyline / narrative spine

Capture the paper's story as a structured chain, not just a summary.

Recommended fields:

```json
{
  "problem": "What problem or pain point motivates the work?",
  "gap": "What is missing or flawed in prior work?",
  "core_insight": "What is the paper's central idea?",
  "method_move": "What technical move implements the insight?",
  "evidence_move": "What evidence is used to prove the method works?",
  "main_takeaway": "What should AC/reviewers remember?",
  "scope_boundary": "What the paper does not claim"
}
```

Also store a 3-level version:

- `one_sentence_story`: concise author-facing story
- `three_bullet_story`: problem / method / evidence
- `logic_chain`: ordered premises leading to the main claim

### 3. Contribution ledger

For each contribution, store:

- `contribution_id`
- exact or near-exact paper wording
- plain-language interpretation
- type: `method|dataset|benchmark|theory|analysis|system|application|empirical_finding`
- novelty basis claimed by the paper
- evidence anchors: sections, figures, tables, equations
- potential reviewer challenge: novelty, significance, missing comparison, clarity, scope, etc.
- confidence

### 4. Claim ledger and claim-evidence map

Every rebuttal-relevant claim needs an ID.

Claim types:

- `problem_claim`: why the problem matters
- `gap_claim`: what prior work lacks
- `method_claim`: what the method does
- `performance_claim`: empirical improvement
- `efficiency_claim`: speed/compute/parameter/memory benefit
- `robustness_claim`: generalization, stability, noise/domain shift
- `analysis_claim`: ablation or diagnostic explanation
- `limitation_claim`: admitted boundary
- `scope_claim`: what is and is not promised

For each claim:

```json
{
  "claim_id": "C01",
  "claim_type": "performance_claim",
  "claim_text": "...",
  "source_anchor": "PAPER:sec4:main-results",
  "evidence_refs": ["TABLE:1", "EXP:nuscenes:main"],
  "strength": "central|supporting|minor",
  "confidence": "high|medium|low",
  "reviewer_challenge_likelihood": "high|medium|low",
  "safe_rebuttal_use": "can cite directly|needs caveat|do not use yet"
}
```

### 5. Method memory

Record the method so later responses use the right technical language.

Include:

- method name and acronym
- module/component list
- pipeline order
- training objectives/losses
- inference procedure
- inputs/outputs
- assumptions
- complexity or implementation notes if stated
- relation to baselines/prior work
- equations/algorithms anchors
- what is genuinely new vs reused standard machinery

### 6. Experiment matrix

This is critical for rebuttal. Build a structured matrix of what was tested.

For each experiment group:

```json
{
  "experiment_id": "EXP01",
  "purpose": "main comparison|ablation|sensitivity|robustness|efficiency|qualitative|user study|case study",
  "dataset": "...",
  "task": "...",
  "metrics": ["..."],
  "baselines": ["..."],
  "methods_compared": ["ours", "baseline A", "baseline B"],
  "table_or_figure": "TABLE:1",
  "result_summary": "...",
  "exact_values_available": true,
  "source_anchor": "PAPER:tab1",
  "rebuttal_value": "high|medium|low"
}
```

Must capture:

- datasets and splits
- metrics and whether higher/lower is better
- baselines and why they are relevant
- SOTA comparisons
- ablation variants and what each removes/adds
- hyperparameter/sensitivity studies
- statistical significance or variance if reported
- qualitative examples and what they are meant to show
- efficiency/resource results if reported
- negative or mixed results if present

### 7. Result ledger

For exact quantitative data, preserve numbers faithfully.

Each result row should include:

- `result_id`
- dataset/task/split
- metric
- compared method/baseline
- our value
- baseline value
- absolute difference when directly computable
- relative difference only if explicitly stated or safely computed and marked
- rank/SOTA status if claimed
- source table/figure/line
- caveat: variance, single run, missing significance, approximate plot reading, etc.

Rules for numbers:

- Do not round beyond the paper's precision unless explicitly marking normalized display.
- Do not infer significance from a small numeric gap.
- Do not claim SOTA unless the paper says it or the comparison table clearly supports it.
- If extracting from a plot visually, mark as `approximate_from_figure`.

### 8. Figure/table index

Create an index of paper artifacts likely useful in rebuttal:

- table/figure ID
- caption or short description
- what claim it supports
- key numbers or visual takeaway
- likely reviewer concerns it can answer
- whether it is safe to cite in author response

### 9. Domain terminology and wording memory

Preserve exact field-specific language because rebuttal tone depends on using the paper's vocabulary.

Record:

- task names and subtask names
- dataset names and official spellings
- metric names, abbreviations, and directionality
- method/module names and acronyms
- baseline names and families
- domain-specific verbs/nouns the paper uses
- preferred phrasing for the contribution
- terms to avoid because they overclaim or conflict with the paper
- ambiguity-prone terms that need definition in rebuttal

Example:

```json
{
  "term": "planning collision rate",
  "category": "metric",
  "canonical_spelling": "...",
  "meaning_in_paper": "...",
  "directionality": "lower_is_better",
  "source_anchor": "PAPER:sec4:metrics",
  "safe_usage_note": "Use with horizon/split when citing."
}
```

### 10. Limitations and weak points

Record limitations honestly. They often become the safest rebuttal material.

Fields:

- explicit paper limitations
- implicit limitations visible from experiments
- missing baselines or datasets
- small gains / variance sensitivity
- assumptions not validated
- failure cases
- reproducibility constraints
- claims that should be softened

Mark each as:

- `already_acknowledged`
- `can_clarify`
- `needs_new_evidence`
- `should_concede`
- `avoid_overclaiming`

### 11. Rebuttal relevance map

Do not analyze reviewers yet, but prepare paper-side evidence for common concern categories.

Concern categories:

- novelty
- significance / small gain
- missing baseline
- dataset bias / limited setting
- metric choice
- statistical significance
- ablation sufficiency
- reproducibility
- clarity / terminology confusion
- overclaiming
- scope / venue fit

For each category, list paper evidence that may help, plus caveats.

## Procedure

### Step 1. Confirm usable paper source

Use `source_manifest.json` and workspace inspection.

Proceed when at least one is available:

- current PDF
- current LaTeX source
- sufficient user-provided paper summary

Stop and ask if paper source is absent or version ambiguous.

### Step 2. Extract structure before details

Identify:

- title / abstract
- section headings
- contribution paragraph
- method section structure
- experiment section structure
- conclusion / limitations
- appendix/supplement if available

Write a short structure outline before extracting claims.

### Step 3. Reconstruct narrative spine

Extract the story in this order:

1. problem
2. prior-work gap
3. core insight
4. method design
5. evidence design
6. claimed outcome
7. boundary / limitation

Keep this separate from the agent's own interpretation. If you infer a link, label it as `inference` and provide rationale.

### Step 4. Build contribution and claim ledgers

Use paper anchors for every contribution and claim. If a claim is important but weakly supported, keep it and mark confidence low; do not delete it.

### Step 5. Build experiment matrix and result ledger

Work table-by-table and figure-by-figure.

For each table:

- identify dataset/task/split
- identify metrics and directionality
- list baselines/methods compared
- extract our method values and key baseline values
- state what the table is intended to prove
- note missing comparisons or caveats

For ablations:

- name each variant
- say what component is removed/changed
- link variant to method component
- record numeric effect if available

### Step 6. Build terminology memory

Extract exact wording for:

- method acronym and expansions
- task/dataset/metric names
- baseline spellings
- phrases the paper uses for novelty and contribution
- cautious language around limitations

### Step 7. Record rebuttal hooks without strategy

Create category-to-evidence hooks, but do not decide how to respond to actual reviewers yet.

Example:

```json
{
  "concern_category": "missing baseline",
  "paper_side_evidence": ["TABLE:2 includes X/Y/Z"],
  "caveat": "Does not include method Q; may require explanation or new experiment.",
  "status": "available|partial|missing"
}
```

### Step 8. Persist outputs

Write:

- `.awesome-rebuttal/memory/paper_memory.json`
- `.awesome-rebuttal/logs/paper_memory_build_report.md`
- optional `.awesome-rebuttal/snapshots/paper_memory_summary.md`

Update `.awesome-rebuttal/memory/project_memory.json`:

- add/update paper source status
- add paper memory path
- add paper-related source IDs to `source_index`
- add open questions for missing paper facts

## Output schema sketch

```json
{
  "version": "0.1",
  "status": "complete|partial|blocked",
  "paper_identity": {},
  "source_status": {},
  "narrative": {
    "one_sentence_story": "",
    "three_bullet_story": [],
    "problem": "",
    "gap": "",
    "core_insight": "",
    "method_move": "",
    "evidence_move": "",
    "main_takeaway": "",
    "scope_boundary": "",
    "logic_chain": []
  },
  "contribution_ledger": [],
  "method_memory": {},
  "experiment_matrix": [],
  "result_ledger": [],
  "figure_table_index": [],
  "terminology": [],
  "claim_evidence_map": [],
  "limitations_and_weak_points": [],
  "rebuttal_relevance_map": [],
  "open_questions": []
}
```

## Paper-source questionnaire

Use this when the paper source is missing or ambiguous:

```markdown
## Need your input: paper source for memory building

I need the current submitted paper before building reliable paper memory.

I found:
- Paper candidates: <paths or none>
- Possible LaTeX roots: <paths or none>
- Possible PDFs: <paths or none>

1. Which source should be treated as the current submitted paper?
   - A. `<path>`
   - B. `<path>`
   - C. I will copy/upload the current PDF or LaTeX into `Paper/`
   - D. Use my pasted summary temporarily, with low confidence

2. If there are multiple versions, which one matches the reviewed submission?
   - A. Latest PDF
   - B. LaTeX source at `<path>`
   - C. I will identify the reviewed version manually
```

## Output report

```markdown
## Paper Memory Build Report

- Status: complete|partial|blocked
- Paper source: ...
- Source confidence: high|medium|low
- Storyline extracted: yes/no
- Contributions extracted: <count>
- Claims extracted: <count>
- Experiment groups extracted: <count>
- Result rows extracted: <count>
- Tables/figures indexed: <count>
- Terminology entries: <count>
- Limitations/weak points: <count>
- Rebuttal relevance hooks: <count>
- Open questions:
  - ...
- Files written:
  - `.awesome-rebuttal/memory/paper_memory.json`
  - `.awesome-rebuttal/logs/paper_memory_build_report.md`
```

## Stop / proceed rules

Proceed to `04_code_memory_builder.md` or `05_review_normalizer.md` when:

- paper memory is complete or sufficiently partial for analysis,
- all central claims have anchors or are marked low-confidence,
- experiments/results are either extracted or explicitly marked missing.

Proceed with warning when:

- paper memory is based only on a user summary,
- some tables/figures are unreadable,
- exact values are unavailable but qualitative claims are still traceable.

Stop and ask when:

- no paper source or summary exists,
- multiple candidate paper versions exist and current submission is unclear,
- table values are ambiguous and would affect rebuttal claims,
- the user wants final drafting but venue rules or paper evidence are not confirmed.

## Quality bar

A high-quality paper memory should let a future agent answer:

- What is the paper's story in one sentence?
- What logical chain supports that story?
- What exactly did the authors claim?
- Which tables/figures/results support each claim?
- Which datasets, metrics, baselines, and ablations were used?
- What are the exact numbers and caveats?
- What domain terminology should be preserved in rebuttal writing?
- Which paper-side evidence can help with common reviewer concern types?

## Safety rules

- Never invent or inflate paper claims.
- Never invent experimental results or statistical significance.
- Never hide weak points; record them as rebuttal constraints.
- Preserve exact numbers, metric directionality, and dataset/split names.
- Mark all inferred story links or approximate values explicitly.
- Keep paper memory local under `.awesome-rebuttal/`; do not expose private paper content externally.
