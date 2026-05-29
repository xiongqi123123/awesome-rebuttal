# 04 Code Memory Builder

## Goal

Build a durable, evidence-grounded memory of the implementation: the overall code architecture, where each claimed innovation is inserted, how it is implemented, which configs/hyperparameters control it, how training/evaluation runs, and what reproducibility or experiment constraints matter for rebuttal.

This capability turns a local codebase into code-side evidence for later strategy, experiment triage, and response writing. It must distinguish what the code actually shows from what the paper claims.

## Boundary

### This capability does

- map repository roots, framework stack, modules, configs, scripts, and data pipelines
- reconstruct the implementation architecture from code evidence
- identify innovation candidates and their insertion points in the pipeline/model/training loop
- record files/classes/functions/config keys that implement each innovation
- extract relevant hyperparameters, thresholds, loss weights, dataset settings, training schedules, and evaluation settings
- link paper claims to code anchors when paper memory is available
- build reproducibility commands and feasibility notes without running expensive jobs
- record missing, stale, or unverified implementation evidence
- write `.awesome-rebuttal/memory/code_memory.json`

### This capability does not

- run training, evaluation, data conversion, or GPU-heavy commands unless explicitly asked
- assume code proves a paper claim without matching paper evidence from `03_paper_memory_builder.md`
- infer performance numbers from code unless result logs explicitly contain them
- modify user code, configs, or checkpoints
- expose private code outside the local workspace
- decide rebuttal strategy or draft final text

## Inputs

Read these first:

- `.awesome-rebuttal/memory/project_memory.json`
- `.awesome-rebuttal/memory/source_manifest.json`
- `.awesome-rebuttal/memory/paper_memory.json` if available
- `.awesome-rebuttal/logs/missing_information_report.md`
- mapped code directories from 00/02, usually `Code/`
- README, docs, scripts, config files, result logs, and source files in the codebase

If no code is available and the rebuttal does not depend on code evidence, write a minimal unavailable memory and continue. If reviewer concerns involve reproducibility, implementation, or experiments, missing code becomes a confidence gap or blocker for those claims.

## Evidence classes

Collect code evidence into these classes:

| Class | Examples | Rebuttal use |
|---|---|---|
| `repo_identity` | repo root, branch, commit, dirty status, framework | reproducibility context |
| `architecture` | model registry, backbone/head modules, pipeline graph | explain how method is built |
| `innovation_impl` | new modules, losses, heads, data processing, training stages | support novelty/implementation claims |
| `insertion_point` | where the innovation plugs into model/data/training/eval | answer “where is it implemented?” |
| `hyperparameter` | config keys, loss weights, thresholds, schedules | answer sensitivity/config questions |
| `entrypoint` | train/test/eval scripts, shell wrappers | reproduce or run extra experiments |
| `dataset_pipeline` | converters, dataset classes, transforms, splits | answer data/bias/reproducibility concerns |
| `evaluation` | metrics, evaluators, benchmark scripts | connect results to code |
| `result_log` | saved logs, tables, checkpoints metadata | support completed experiment claims |
| `environment` | requirements, Docker/env docs, CUDA/Python stack | reproducibility feasibility |
| `risk` | missing files, hardcoded paths, undocumented steps | rebuttal constraints |

## Core memory model

### 1. Codebase identity

Record for each repo:

- path
- availability
- git branch / commit / dirty status if cheap and safe
- language stack
- framework stack
- package/environment files
- README/docs availability
- likely license or external base code if obvious
- confidence and caveats

Do not run network installs or environment setup from this capability.

### 2. Architecture map

Build a high-level map of the implementation.

Recommended fields:

```json
{
  "architecture_id": "ARCH01",
  "name": "overall model/training architecture",
  "summary": "...",
  "layers": [
    {
      "stage": "data|model_backbone|neck|head|loss|training_loop|evaluation|visualization",
      "components": ["..."],
      "files": ["CODE:path#anchor"],
      "inputs": ["..."],
      "outputs": ["..."],
      "notes": []
    }
  ],
  "framework_patterns": ["registry", "config-driven", "two-stage training"]
}
```

Capture both static architecture and runtime pipeline:

- data conversion / loading
- augmentation / preprocessing
- model construction
- forward pass components
- loss computation
- training stages
- inference / post-processing
- evaluation metrics
- visualization / qualitative outputs

### 3. Innovation implementation map

This is the central output. For each claimed or suspected innovation, store:

```json
{
  "innovation_id": "INNOV01",
  "name": "...",
  "status": "paper_linked|code_detected_pending_paper_link|user_confirmed|uncertain",
  "paper_claim_refs": ["C01"],
  "implementation_summary": "How the idea is implemented in code.",
  "insertion_point": {
    "pipeline_stage": "data|model|loss|training|inference|evaluation",
    "parent_component": "...",
    "before": "What happens before this insertion",
    "after": "What consumes its output"
  },
  "code_anchors": ["CODE:path#class_or_function"],
  "config_anchors": ["CODE:path#config_key"],
  "hyperparameters": ["HP01", "HP02"],
  "expected_effect": "What this innovation is supposed to improve.",
  "ablation_refs": ["EXP/PAPER refs if available"],
  "verification_status": "implemented|partially_implemented|declared_not_traced|not_found",
  "confidence": "high|medium|low",
  "rebuttal_use": "can cite implementation|needs paper/code alignment|do not cite yet"
}
```

Important distinctions:

- `paper_linked`: paper memory claim and code anchor align.
- `code_detected_pending_paper_link`: code appears novel or custom, but paper source is unavailable or not yet linked.
- `uncertain`: name suggests relevance but implementation path is not clear.
- `not_found`: paper claim exists but no code anchor found.

### 4. Config and hyperparameter ledger

Extract hyperparameters that may matter in rebuttal or reproduction.

Sources:

- `*.py` config files
- `*.yaml`, `*.yml`, `*.json`, `*.toml`
- shell scripts with command-line flags
- README examples
- constants in source files if they control behavior

Record:

```json
{
  "hyperparameter_id": "HP01",
  "name": "loss_weight_x",
  "value": "...",
  "type": "loss_weight|threshold|schedule|optimizer|dataset|augmentation|architecture|runtime|evaluation",
  "defined_in": "CODE:path#anchor",
  "used_by": ["INNOV01", "ARCH01"],
  "default_or_experiment_specific": "default|experiment_specific|unknown",
  "sensitivity_evidence": "available|not_reported|unknown",
  "safe_rebuttal_note": "..."
}
```

Pay special attention to:

- learning rate, optimizer, batch size, epochs/iterations
- loss weights and auxiliary losses
- thresholds, margins, top-k, NMS/post-processing settings
- model dimensions, number of layers, queries, anchors, heads
- dataset version/split/sample interval
- augmentation settings
- training stages and checkpoint dependencies
- evaluation horizon, metric thresholds, matching thresholds
- seeds and determinism controls

### 5. Entrypoint and command memory

Record runnable commands without executing heavy jobs.

Include:

- data preparation scripts
- single-GPU and distributed train commands
- test/evaluation commands
- visualization commands
- benchmark scripts
- config arguments
- expected outputs/log locations
- compute assumptions: GPU count, memory, dataset paths, checkpoints

Mark each command:

- `safe_to_run_lightweight`
- `expensive_requires_user_approval`
- `requires_dataset_or_checkpoint`
- `unknown`

### 6. Dataset and evaluation pipeline memory

Record:

- dataset classes and converters
- expected directory layout
- preprocessing and filtering
- splits and temporal horizons
- metrics and evaluator files
- external benchmark compatibility
- result serialization format
- known hardcoded paths or dataset assumptions

This helps later answer reviewer concerns about dataset bias, metrics, reproducibility, and missing baselines.

### 7. Claim-code map

When `paper_memory.json` exists, link each relevant claim to implementation anchors.

```json
{
  "claim_id": "C01",
  "claim_text": "...",
  "code_refs": ["CODE:path#anchor"],
  "config_refs": ["CODE:path#config_key"],
  "test_or_result_refs": ["LOG:path#anchor"],
  "support_level": "direct|indirect|not_found|not_applicable",
  "confidence": "high|medium|low",
  "notes": []
}
```

If paper memory is blocked/missing, create a provisional `code_to_possible_claims` list instead of claiming alignment.

### 8. Experiment feasibility map

Prepare for `10_experiment_triage.md` by recording what the code can likely run.

For each feasible experiment:

- experiment type: baseline rerun, ablation, sensitivity, additional metric, visualization, sanity check
- command/config needed
- expected cost: low/medium/high/unknown
- dependencies: dataset, checkpoint, GPU, time
- output expected
- risk of not reproducing
- whether it answers likely reviewer concerns

Do not decide priority here; just prepare feasibility evidence.

### 9. Reproducibility and risk ledger

Record issues that can constrain rebuttal promises:

- missing README or incomplete install instructions
- missing checkpoint/dataset path
- hardcoded absolute paths
- unavailable baseline code
- nondeterministic seeds
- config/result mismatch
- custom CUDA ops or compiled dependencies
- unclear training stage dependencies
- result logs absent
- code diverges from paper terminology

Mark each risk:

- `blocks_reproduction`
- `reduces_confidence`
- `minor_documentation_gap`
- `needs_user_input`

## Procedure

### Step 1. Confirm code scope

Use the workspace map and `source_manifest.json` to identify repo roots under the code directory.

If multiple repos exist, classify them:

- main implementation
- baseline/submodule
- scripts/tools only
- unrelated/reference code

Ask only if multiple plausible main repos exist and the choice affects memory.

### Step 2. Inventory repository structure

Read lightweight files first:

- README / docs / quick start
- requirements / environment files
- config directories
- scripts / shell wrappers
- tools train/test/eval files
- package/module top-level structure

Avoid loading every source file. Search for names from paper memory, config keys, registries, custom modules, losses, dataset classes, and evaluation functions.

### Step 3. Identify framework and architecture pattern

Look for:

- config-driven frameworks
- registries/builders
- model classes
- dataset/evaluator classes
- train/test entrypoints
- staged training configs
- plugin directories

Write the high-level architecture map before drilling into innovations.

### Step 4. Extract innovation candidates

Sources for candidates:

- paper contributions/claims from 03
- custom class/module names
- config names
- project/repo name
- ablation config variants
- comments/docstrings/README descriptions
- files changed relative to an obvious base framework, if identifiable

For each candidate, trace:

1. where it is configured,
2. where it is instantiated,
3. where it executes in forward/training/evaluation,
4. what inputs/outputs it touches,
5. what hyperparameters control it,
6. how it could be disabled/ablated if config supports that.

### Step 5. Extract hyperparameters and configs

For each main config:

- model config
- data config
- optimizer and schedule
- loss weights
- training/evaluation settings
- checkpoint/load paths
- custom flags

Record exact values with file anchors. If config imports/base-inherits another config, record inheritance when obvious.

### Step 6. Extract entrypoints and commands

Record commands from README/scripts without running heavy jobs.

If a lightweight syntax/import check is useful, only run it when safe and local. Do not run training/evaluation/data conversion by default.

### Step 7. Build claim-code or provisional code-claim map

If `paper_memory.json` is complete/partial, link paper claims to code anchors.

If paper memory is blocked, produce:

- `code_detected_innovations`
- `possible_paper_claim_links`: empty or low-confidence
- open question: “Need paper source to align code innovations with claims.”

### Step 8. Persist outputs

Write:

- `.awesome-rebuttal/memory/code_memory.json`
- `.awesome-rebuttal/logs/code_memory_build_report.md`
- optional `.awesome-rebuttal/snapshots/code_memory_summary.md`

Update `.awesome-rebuttal/memory/project_memory.json`:

- code memory path
- code availability
- code evidence confidence
- open questions and reproduction risks
- source index additions for important code anchors

## Output schema sketch

```json
{
  "version": "0.1",
  "status": "complete|partial|blocked|unavailable",
  "codebase": {
    "path": "Code/main-repo",
    "available": true,
    "language_stack": ["Python"],
    "framework_stack": ["..."],
    "git": {}
  },
  "architecture_map": [],
  "innovation_implementation_map": [],
  "config_hyperparameter_ledger": [],
  "entrypoints": [],
  "reproduction_commands": [],
  "dataset_pipeline": [],
  "evaluation_pipeline": [],
  "result_log_index": [],
  "claim_code_map": [],
  "code_to_possible_claims": [],
  "experiment_feasibility_map": [],
  "reproducibility_risks": [],
  "open_questions": []
}
```

## Code-scope questionnaire

Use this when the code scope or main repo is ambiguous:

```markdown
## Need your input: code memory scope

I found:
- Candidate code repos: <paths>
- Config directories: <paths>
- Train/eval scripts: <paths>
- Possible result logs/checkpoints: <paths or none>

1. Which repo is the implementation for the submitted paper?
   - A. `<path>`
   - B. `<path>`
   - C. Multiple repos; map them as main + baselines
   - D. Code is not needed for this rebuttal

2. Should I treat config files as authoritative for hyperparameters?
   - A. Yes, use current configs
   - B. No, I will identify the reviewed-submission configs
   - C. Use configs only as low-confidence implementation evidence

3. Are expensive runs allowed later if experiment triage recommends them?
   - A. Yes, but ask before running
   - B. No, only inspect code/logs
   - C. Maybe; decide per experiment
```

## Output report

```markdown
## Code Memory Build Report

- Status: complete|partial|blocked|unavailable
- Main repo: ...
- Framework/language stack: ...
- Architecture components indexed: <count>
- Innovation candidates traced: <count>
- Hyperparameters/config entries extracted: <count>
- Entrypoints/commands indexed: <count>
- Dataset/evaluation pipeline entries: <count>
- Claim-code links: <count>
- Provisional code-claim links: <count>
- Experiment feasibility entries: <count>
- Reproducibility risks: <count>
- Open questions:
  - ...
- Files written:
  - `.awesome-rebuttal/memory/code_memory.json`
  - `.awesome-rebuttal/logs/code_memory_build_report.md`
```

## Stop / proceed rules

Proceed when:

- main repo is identified or code is explicitly unavailable,
- architecture map is sufficient for current rebuttal needs,
- innovations are either traced or marked `not_found/uncertain`,
- hyperparameters relevant to claimed innovations are recorded or marked missing,
- no heavy command has been run without user approval.

Proceed with warning when:

- paper memory is missing, so innovation links are provisional,
- code is available but result logs/checkpoints are absent,
- configs may not match reviewed submission,
- implementation is framework-heavy and some instantiation paths remain indirect.

Stop and ask when:

- multiple candidate main repos/configs exist and choice changes evidence,
- user asks for reproduction but dataset/checkpoint paths are unknown,
- a heavy command would be needed to verify a claim,
- code appears to conflict with paper memory in a way that affects rebuttal claims.

## Quality bar

A high-quality code memory should let a future agent answer:

- What is the overall implementation architecture?
- Where is each innovation inserted in the data/model/loss/training/evaluation pipeline?
- Which files/classes/functions implement it?
- Which config keys and hyperparameters control it?
- How do we train/evaluate/reproduce the reported setup?
- Which paper claims have direct code support, indirect support, or no code support?
- What extra experiments are feasible from the current codebase?
- What reproducibility risks should constrain rebuttal promises?

## Safety rules

- Never run expensive commands without explicit user approval.
- Never claim an innovation is implemented unless code anchors support it.
- Never claim code results exist unless logs/results/checkpoints show them.
- Keep provisional code-only findings separate from paper-linked claims.
- Preserve exact config values and file anchors.
- Record unknowns instead of filling gaps with assumptions.
