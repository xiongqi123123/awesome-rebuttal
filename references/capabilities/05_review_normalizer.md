# 05 Review Index Builder

## Goal

Convert raw reviewer comments into a neutral, traceable review index. This capability stores each reviewer’s original opinion, extracts reviewer-provided metadata, builds raw anchors, and creates a common-issue index showing which reviewers mentioned the same topic.

This is an indexing layer, not an analysis layer. It should answer: “What did each reviewer say, where did they say it, and which topics recur across reviewers?” It should not decide rebuttal strategy, reviewer persuadability, severity, AC priority, or whether a reviewer is right.

## Design lessons from rebuttal workflows

Successful rebuttal tools separate mechanical organization from strategic judgment:

- Keep raw reviews verbatim before any transformation.
- Ensure every later issue maps back to a reviewer and raw quote anchor.
- Track shared issues and reviewer-specific issues so coverage can be audited.
- Do not let any concern disappear when moving from raw reviews to response planning.

## Boundary

### This capability does

- preserve raw review text per reviewer
- assign an internal stable label (`R1`, `R2`, ...) and separately preserve the platform anonymous reviewer ID when present
- extract reviewer metadata when explicitly present: score, rating, confidence, fit, technical quality, presentation
- segment each review into source sections such as strengths, weaknesses, review, questions, minor issues, fit justification
- create stable raw anchors for reviewer statements
- build neutral issue items from reviewer wording
- group recurring issue topics into a common-issue index and list reviewer sources
- record missing metadata as `unknown`
- write `.awesome-rebuttal/memory/review_memory.json`

### This capability does not

- judge whether a concern is valid
- label reviewers as pivotal, hostile, persuadable, or supportive
- assign strategic severity or response priority
- infer misunderstanding unless the reviewer explicitly says something factually checkable and it is marked only as `possible_check_needed`
- decide whether an experiment is needed
- propose rebuttal wording or response mode
- merge away reviewer-specific nuance

## Inputs

Read these first:

- `.awesome-rebuttal/memory/project_memory.json`
- `.awesome-rebuttal/memory/source_manifest.json`
- raw review files under the mapped reference path, usually `Reference/`
- pasted review text from the current session, if any
- venue review rubric only if already user-confirmed or present in the review packet

If raw reviews are missing, stop and ask for them. Do not synthesize review content from memory.

## Neutral extraction principles

Use only information present in the review text.

Allowed neutral labels:

- `identity`: internal stable label and platform anonymous reviewer ID
- `metadata`: score, confidence, fit, technical-quality rating, presentation rating
- `section`: strengths, weaknesses, review/body, questions, minor issues, fit justification
- `topic_tag`: novelty, baseline, dataset/subset, metric/statistics, safety claim, physical feasibility, closed-loop result, efficiency, generalization, reproducibility, clarity, venue fit, experiment request, limitation, other
- `issue_form`: assertion, question, request, praise, summary, metadata
- `evidence_anchor`: raw quote, section name, line/paragraph index

Avoid analysis labels in 05:

- no `critical/major/minor`
- no `pivotal`
- no `high/medium/low decision relevance`
- no `misunderstanding/true limitation`
- no `response mode`
- no `strategy`

Semantic labels belong in `06_situation_analyzer.md`; priority, importance, and posture labels belong in `07_concern_atomizer.md`.

## Core memory model

### 1. Review packet identity

Record:

- source file(s)
- venue/submission ID if present
- extraction timestamp
- reviewer count
- parsing confidence
- unresolved parsing questions

### 2. Reviewer raw memory

For each reviewer:

```json
{
  "reviewer_id": "R1",
  "stable_label": "R1",
  "anonymous_id": "<anonymous_reviewer_id_or_unknown>",
  "anonymous_id_source": "review_heading|openreview_signature|user_provided|unknown",
  "source_path": "Reference/reviews.md",
  "raw_review_text": "verbatim review block or path pointer if too large",
  "raw_text_storage": "inline|external_path",
  "metadata": {
    "rating": "2: Weak Reject",
    "confidence": "4: Expert",
    "fit": "2: Small audience",
    "technical_quality": "2: Medium",
    "technical_presentation": "3: Fair"
  },
  "sections": [],
  "raw_anchors": [],
  "missing_fields": []
}
```

For long reviews, store the raw text in `.awesome-rebuttal/memory/raw_reviews/<stable_label>.md` and keep a path pointer in JSON. Keep the anonymous reviewer ID in metadata, not as the only file name, so response planning remains stable even if platform IDs are awkward or missing.

### 3. Section index

Segment each reviewer into sections if headings are present. Keep the original heading names.

Common sections:

- `Strengths`
- `Weaknesses`
- `Review`
- `Questions`
- `Minor Issues`
- `Fit`
- `Fit Justification`
- `Rating`
- `Confidence`

For each section:

```json
{
  "section_id": "R1:S2",
  "reviewer_id": "R1",
  "section_name": "Weaknesses",
  "raw_anchor": "REVIEW:R1:Weaknesses",
  "text": "...",
  "item_count": 4
}
```

### 4. Raw anchor map

Every extracted statement gets a raw anchor:

```json
{
  "anchor_id": "REVIEW:R1:Weaknesses:W1",
  "reviewer_id": "R1",
  "section_id": "R1:S2",
  "quote": "Limited novelty – mostly a combination of existing techniques",
  "location_hint": "Weaknesses item 1",
  "source_path": "Reference/reviews.md"
}
```

Quote length should be enough to identify the original concern but not so long that the JSON becomes unreadable. Preserve full raw review separately.

### 5. Issue item index

Create neutral issue items from reviewer statements. An issue item is not yet a strategic atomic concern; it is an indexed reviewer statement or request.

```json
{
  "issue_item_id": "RI:R1:001",
  "reviewer_id": "R1",
  "section_name": "Weaknesses",
  "raw_anchor": "REVIEW:R1:Weaknesses:W1",
  "short_label": "limited novelty / combination of existing techniques",
  "topic_tags": ["novelty", "method_design"],
  "issue_form": "assertion|question|request|praise|summary",
  "verbatim_or_close_quote": "...",
  "explicit_requested_action": "none|explain|add_baseline|add_sensitivity|provide_statistics|clarify_wording|other",
  "notes": []
}
```

Rules:

- Split only when the reviewer clearly raises separable points.
- Preserve compound context by linking related issue items through `related_issue_item_ids` if useful.
- If an item is praise, keep it as praise; supportive evidence matters later.
- If an item is a minor writing issue, keep it with a topic tag and low-level form, not a strategic priority.

### 6. Common issue index

Group issue items by recurring topic without strategic interpretation.

```json
{
  "common_issue_id": "CI:novelty-loss-engineering",
  "neutral_label": "novelty / loss-function engineering concern",
  "topic_tags": ["novelty", "method_design"],
  "mentioned_by": ["R1", "R2", "R3", "R5"],
  "issue_item_ids": ["RI:R1:001", "RI:R2:001"],
  "representative_quotes": [
    {"reviewer_id": "R1", "raw_anchor": "...", "quote": "..."}
  ],
  "variation_notes": "Neutral description of how wording differs; no priority judgment."
}
```

Common-issue grouping should preserve reviewer-specific differences:

- same high-level topic but different requested action → same common issue with variation notes, or separate if response would differ materially later
- one reviewer asks a question while another asserts criticism → keep both item forms
- praise and criticism on same topic can be linked but not collapsed

## Topic tag guide

Use descriptive topic tags only:

- `novelty`
- `method_design`
- `theory_or_motivation`
- `safety_claim`
- `physical_feasibility`
- `margin_or_threshold`
- `horizon_weighting`
- `baseline_coverage`
- `missing_comparison`
- `dataset_subset`
- `selection_bias`
- `metric_or_statistics`
- `small_gain`
- `closed_loop_evaluation`
- `efficiency_tradeoff`
- `generalization`
- `reproducibility`
- `clarity_wording`
- `venue_fit`
- `positive_evidence`
- `other`

## Procedure

### Step 1. Locate raw reviews

Use `source_manifest.json` and `Reference/`. If multiple candidate review files exist, pick the user-confirmed one or ask.

### Step 2. Preserve raw packet

Write or update:

- `.awesome-rebuttal/memory/reviews_raw.md`
- `.awesome-rebuttal/memory/raw_reviews/<stable_label>.md` when splitting by reviewer

Never edit reviewer wording except for safe formatting around headings.

### Step 3. Split reviewers

Detect reviewer boundaries using headings, IDs, OpenReview labels, or user-provided labels.

Always assign stable labels `R1`, `R2`, etc. for internal references. Separately extract the anonymous reviewer ID from the review heading/signature when present; if unavailable, set `anonymous_id: "unknown"`.

### Step 4. Extract metadata and sections

Extract explicit metadata only. Missing values stay `unknown`.

### Step 5. Create issue items

For each reviewer section, create neutral issue items. Keep praise, criticisms, questions, and requests distinguishable.

### Step 6. Build common issue index

Cluster issue items by topic and wording overlap. This is an index, so do not assign strategic severity. The output should simply show which reviewers mentioned which topics.

### Step 7. Persist memory

Write:

- `.awesome-rebuttal/memory/review_memory.json`
- `.awesome-rebuttal/logs/review_index_report.md`

Update `.awesome-rebuttal/memory/project_memory.json`:

- review memory path
- reviewer count
- review source path(s)
- open parsing questions

## Output schema sketch

```json
{
  "version": "0.1",
  "status": "complete|partial|blocked",
  "review_packet": {},
  "reviewers": [],
  "section_index": [],
  "raw_anchor_map": [],
  "issue_item_index": [],
  "common_issue_index": [],
  "metadata_summary": {},
  "parser_notes": [],
  "open_questions": []
}
```

## Output report

```markdown
## Review Index Report

- Status: complete|partial|blocked
- Review source(s): ...
- Reviewers indexed: <count>
- Raw review files written: <count>
- Metadata extracted:
  - ratings: <count>/<reviewer_count>
  - confidence: <count>/<reviewer_count>
- Issue items indexed: <count>
- Common issue groups: <count>
- Parsing uncertainties:
  - ...
- Files written:
  - `.awesome-rebuttal/memory/review_memory.json`
  - `.awesome-rebuttal/memory/reviews_raw.md`
  - `.awesome-rebuttal/logs/review_index_report.md`
- Next route: `06_situation_analyzer.md`
```

## Stop / proceed rules

Proceed to 06 when:

- raw reviews are preserved,
- reviewers are split with stable labels,
- issue items have raw anchors,
- common issue index lists reviewer sources.

Proceed with warning when:

- score/confidence fields are missing,
- review sections are irregular but raw anchors are preserved,
- common issue grouping is partial and marked as such.

Stop and ask when:

- raw reviews are missing,
- reviewer boundaries cannot be inferred,
- multiple review files conflict and no authoritative source is known.

## Safety rules

- Never drop a reviewer concern because it seems minor.
- Never rewrite negative reviewer wording into a softer interpretation.
- Never assign strategic severity or response priority in 05.
- Never fabricate reviewer metadata.
- Preserve raw reviews locally under `.awesome-rebuttal/`.
