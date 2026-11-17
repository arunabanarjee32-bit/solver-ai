# Fine-tuning model research for Solver AI

Research date: **17 November 2026, Asia/Kolkata**.

Status: **comparison for a future decision; no model selected or assumed**.
This document does not authorize downloads, training, paid inference or GPU
provisioning. No weights were downloaded, dependencies installed, models loaded,
training started or benchmarks executed during this research.

## Scope and evidence limits

Solver AI needs to compare algorithmic reasoning, source generation, helpful
tutoring and bounded debugging. These are related capabilities, not one score.
The existing authored hint API and its account UI are implemented; this research
does not reopen that work or describe authored hints as model inference.

The comparison below covers representative relevant families, including older
baselines and newer architectures. It is **not a literal inventory of every model
released, a current leaderboard, or a claim that one model is globally best**.
Other checkpoints can enter the comparison when their official metadata and
relevance are established.

Official GitHub documentation was accessible. Direct requests to official Hugging
Face model APIs/cards were rejected by the environment proxy with **403 Forbidden**;
the Qwen blog was also unavailable. Consequently:

- Model-card revisions, weight/configuration hashes and tokenizer revisions have
  **not been verified**. No Hugging Face commit SHA is invented here.
- The sources were read from mutable GitHub `main` branches on the research date;
  they are cited below, but are not pinned checkpoint manifests.
- Architecture names, sizes and context claims below reflect the named official
  documentation where available. Exact parameter counts, native context, scaling
  settings, output limits and training support still need the selected card/config.
- A source-code repository's Apache or MIT license is **not automatically the
  model-weight license**. Unverified checkpoint terms are marked for review.
- Upstream benchmark claims are not results measured by this project. They are
  not used to declare a winner or to predict a fine-tuning gain.

The publisher's latest repository landing page can change its subject. In
particular, the old `QwenLM/Qwen2.5-Coder` README URL now returns the current
Qwen3-Coder-Next landing document. It cannot verify the original Qwen2.5-Coder
model card, context or license. Legacy checkpoint IDs remain research candidates
until their own original cards/configurations can be inspected.

## What is being compared

**Open-weight adaptation:** a checkpoint can potentially be downloaded and
adapted locally when its license, architecture and toolchain permit. LoRA/QLoRA
support is a separate compatibility question. An inference-only quantization,
GGUF file or FP8 release is not automatically an appropriate training input.

**API-only access:** a provider endpoint can be an external evaluation baseline
or product adapter. An API model name does not grant access to weights or permit
local fine-tuning. Hosted fine-tuning products, when available, have their own
eligibility, data-processing, price and export restrictions.

**Base versus instruction/reasoning checkpoints:** a base code model can support
controlled continued training, but needs suitable instruction formatting and may
require more work to behave as a tutor. An instruction model provides an existing
interaction policy that narrow fine-tuning can damage. Reasoning models may use
special chat templates, output boundaries and longer generation budgets; preserve
their documented format without assuming that visible reasoning is correct.

## Numbered comparison for future evaluation

The numbers are identifiers, **not a ranking**. A family can contain several
releases with different terms and operating requirements.

| No. | Checkpoint or family to research | Official evidence and licensing position | DSA relevance and practical questions |
| --- | --- | --- | --- |
| 1 | `Qwen/Qwen3-4B`, `Qwen/Qwen3-8B`, `Qwen/Qwen3-14B`, `Qwen/Qwen3-32B` | The Qwen3 README lists these dense size tiers and switching between thinking/non-thinking modes for the original release. It states Apache 2.0 for its open-weight models. Exact checkpoint/config revisions remain unverified. [Q1] | Compare a dense general reasoning model's algorithm explanations, code and bounded hints. Smaller dense models are a useful hardware comparison class; larger models require more total training memory. Fix mode, chat template and output budget during evaluation. |
| 2 | `Qwen/Qwen3-4B-Instruct-2507`, `Qwen/Qwen3-4B-Thinking-2507` | Official release links identify separate 4B variants. Updated Instruct is non-thinking only; Thinking is thinking only. The family documents long context with scaling caveats. [Q1] | Compare compact instruction and reasoning variants under equal tasks and an explicit token/cost policy. They are not interchangeable with the original hybrid Qwen3-4B. Longer reasoning output may cost more even at the same parameter count. |
| 3 | `Qwen/Qwen3-30B-A3B-Instruct-2507`, `Qwen/Qwen3-30B-A3B-Thinking-2507` | Official Qwen3 links distinguish these MoE releases and their modes. The family describes 256K context, with extension requiring documented configuration. [Q1] | Potential larger comparison points for planning/reasoning. The roughly 3B active-parameter label concerns computation; it does not mean only 3B weights must be stored or adapted. Verify routing and training-framework support. |
| 4 | `Qwen/Qwen3-Coder-30B-A3B-Instruct` | Official Qwen3-Coder documentation links this coding-focused MoE checkpoint, lists 256K context and states non-thinking behavior. Its exact model-weight license/config still needs direct card verification. [Q2] | Compare code generation and repair against general reasoning models. Agent/repository coding ability does not itself establish competitive-programming or tutoring quality. Total 30B-class weights make memory planning larger than a dense 3B model. |
| 5 | `Qwen/Qwen3-Coder-Next`, `Qwen/Qwen3-Coder-Next-Base` | Current official documentation names both and describes a foundation based on Qwen3-Next-80B-A3B-Base, hybrid attention and MoE, plus 256K native context. Exact artifact revisions and weight terms remain to be checked. [Q2] | Research options for larger infrastructure. An 80B-total/3B-active family is not a small training checkpoint merely because few parameters are active per token. Check hybrid-attention kernels, tokenizer changes and adapter coverage before budgeting. |
| 6 | Legacy `Qwen/Qwen2.5-Coder-7B-Instruct`, `Qwen/Qwen2.5-Coder-14B-Instruct`, `Qwen/Qwen2.5-Coder-32B-Instruct`, and relevant base variants | Candidate identities were requested for comparison, but the old repository URL now serves the newer Coder landing page. Original cards, exact context, revisions and per-checkpoint terms are **pending verification**. [Q3] | Preserve a coding-specialized older baseline in the research plan. Do not assume it loses to every newer general model. Compare actual DSA tasks and teaching behavior; check the original tokenizer/template before adapting it. |
| 7 | `deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B`, `-7B`, `-14B`, `-32B` | Official README identifies dense Qwen-derived distilled checkpoints. It states MIT for its release and notes Apache-licensed Qwen base origins. These are not the 671B full R1 model. Direct card/config revisions remain unverified. [D1] | Useful reasoning-oriented comparison class across several sizes. Reasoning token length, malformed/truncated solutions and template preservation need explicit evaluation. Do not apply the full R1 model's context specification automatically to each distill. |
| 8 | `deepseek-ai/DeepSeek-R1-Distill-Llama-8B`, `-70B` | Official README identifies Llama 3.1 and Llama 3.3 origins respectively and explicitly retains the need to consider their original license terms. [D1] | Contrast reasoning distillation with Qwen-derived alternatives. The 8B size is a manageable research class relative to 70B; inherited Llama obligations are part of eligibility, not erased by the distiller's MIT notice. |
| 9 | `deepseek-ai/DeepSeek-Coder-V2-Lite-Base`, `-Lite-Instruct`; larger `DeepSeek-Coder-V2-Base`/`-Instruct` | Official README lists Lite at 16B total/2.4B active and full at 236B total/21B active, and discusses 128K context. Code is MIT; weights use a separate model agreement. [D2] | A coding-specialized MoE baseline with distinctive architecture/runtime support requirements. Total weights, not only active parameters, determine storage and much of training memory. Full-size models require a different infrastructure tier from a small dense experiment. |
| 10 | `microsoft/Phi-4-mini-instruct`, `microsoft/Phi-4-mini-reasoning`, `microsoft/phi-4`, `microsoft/Phi-4-reasoning` | Microsoft documentation identifies mini models as 3.8B and Phi-4 as 14B. Its family table labels Phi-4-reasoning inconsistently, while the dedicated reasoning recipe calls it 14B. Resolve that inconsistency from the actual card/config. Checkpoint weight licenses/context are not verified by the cookbook's code license. [P1, P2] | Compact tutoring/reasoning comparison points. Evaluate Python/C++ correctness, explanation quality and long-output cost separately. The documentation inconsistency is a reason to verify artifacts, not to silently copy a table entry. |
| 11 | Gemma 3 text/instruction family, including `google/gemma-3-1b-it`, `google/gemma-3-4b-it`, `google/gemma-3-12b-it`, `google/gemma-3-27b-it` | Official PyTorch documentation lists 1B text-only and 4B/12B/27B multimodal variants. It links checkpoint distribution and also shows a `-pytorch` packaging variant. Exact IDs/formats, weight terms and card/config revisions need direct confirmation. [G1] | Possible small/general instruction baselines. A text-only DSA task does not require a vision stack. Verify whether vision modules are loaded/frozen, the correct training implementation and the applicable model-specific terms. |
| 12 | CodeGemma and newer Gemma releases as separate follow-up research | The official PyTorch repository records CodeGemma support. A separate current DeepMind README already demonstrates `Gemma4_E4B` and links a Gemma 4 model card. That implementation example does not verify every current Gemma checkpoint or its size/license. [G1, G2] | Do not mistake the older Gemma 3 list for exhaustive current availability. Investigate specific code-oriented or newer compact artifacts only after obtaining their actual model cards. Keep newer-family uncertainty visible. |
| 13 | `meta-llama/Llama-3.1-8B-Instruct`; smaller Llama 3.2 1B/3B text variants | Meta's family table names sizes and 128K context. The actual Llama 3.1 model card and Community License are accessible on GitHub; this is a custom license with use/redistribution conditions, not Apache/MIT. [L1, L2, L3] | General instruction baselines and ecosystem comparison. DSA skill is an empirical question. Check exact checkpoint terms, access eligibility, formatting and base-versus-Instruct behavior before training. |
| 14 | Llama 4 Scout/Maverick as larger architecture research | Meta's official family table lists Scout-17B-16E and Maverick-17B-128E, with separate Llama 4 license/card links. These are MoE families; 17B active is not total storage. Full artifact metadata was not inspected here. [L1] | Potential future reference points, not assumed single-GPU adaptation targets. Long context and multimodal/agentic capabilities do not eliminate DSA evaluation or compute limits. |
| 15 | `mistralai/Mistral-7B-Instruct-v0.3`, Mistral-NeMo 12B base/instruction releases | Official inference documentation identifies the distributions; the old official fine-tune repository contains relevant recipes but is now explicitly archived. Its NeMo notes warn that vocabulary/loss computation can increase memory. Confirm the exact weight license and maintained trainer before an experiment. [M1, M2] | Older dense baselines that can expose whether a more complicated reasoning/agent architecture is actually needed. Separate inference examples from reproducible training support. |
| 16 | `mistralai/Mistral-Small-3.1-24B-Base-2503`, `-Instruct-2503` | Official inference documentation names both 24B variants. Its library license does not alone establish checkpoint terms; direct cards/configs remain unverified. [M1] | A larger dense general/coding baseline. A 24B model has substantially different training-memory needs from a 7B model, and multimodal packaging may add complexity irrelevant to DSA. |
| 17 | Codestral 22B, Codestral-Mamba 7B and Mathstral 7B as distinct Mistral-family research | Official inference documentation distinguishes these artifacts and explicitly identifies Codestral 22B v0.1's MNPL non-production license. Do not generalize one Mistral model's license to another. [M1] | Code specialization, mathematical reasoning and architecture vary. Mamba training/tool support needs its own check; Codestral v0.1's licensing position may exclude an intended production use. They cannot be treated as interchangeable Apache-licensed checkpoints. |
| 18 | `bigcode/starcoder2-3b`, `bigcode/starcoder2-7b`, `bigcode/starcoder2-15b` | Official README lists code-focused sizes, grouped-query attention, 16,384-token context and 4,096-token sliding-window attention, with a LoRA/4-bit fine-tuning example. The GitHub Apache license covers code; the model-weight license still requires its own card review. [S1] | Useful smaller code-base-model comparison class. It is not automatically an instruction-following tutor. Training data format, attribution/license requirements and instruction adaptation must be evaluated explicitly. |
| 19 | IBM Granite Code base/instruction 3B, 8B, 20B and 34B | Official Granite Code documentation identifies both families and states Apache 2.0 for the models. It lists context-specific checkpoint IDs such as `ibm-granite/granite-3b-code-base-2k` and `ibm-granite/granite-8b-code-instruct-4k`. Direct artifact revisions remain unverified. [I1] | Transparent smaller code-model baselines, with context limits that may affect long statements or repair logs. Compare exact context-tagged releases rather than only the family name. |
| 20 | Closed/API-only models, for example provider-hosted GPT, Claude or Gemini offerings | Provider API access is a separate category from open weights. This research did not verify any particular current API model, pricing, fine-tuning eligibility or export rights. | Potential external reference baselines after explicit privacy/spend approval. They are not local QLoRA candidates unless the provider independently releases suitable weights under appropriate terms. |
| 21 | `openai/gpt-oss-20b`, `openai/gpt-oss-120b` | OpenAI's official README identifies 21B total/3.6B active and 117B total/5.1B active respectively, describes both as fine-tunable and Apache 2.0, and requires the Harmony response format. The repository license was also read. Exact checkpoint/config revisions and maximum context remain unverified here. [O1, O2] | Relevant open-weight reasoning/coding alternatives, including the 20b family named in archived phi-code results. Their low/medium/high reasoning effort changes the resource comparison. The publisher's MXFP4 inference-memory claims of 16 GB and a single 80 GB GPU are not QLoRA training-fit guarantees; verify kernel, quantization and adapter support. |
| 22 | Full `deepseek-ai/DeepSeek-R1` and `deepseek-ai/DeepSeek-R1-Zero` | The official README lists both full MoE models at 671B total/37B active with 128K context, and states MIT for the release. These are separate from the smaller distilled models in rows 7–8. Exact artifact/config revisions remain unverified. [D1] | Potential larger research/reference models when infrastructure and approved budget justify them. They are not small 37B-storage checkpoints and should not be assumed to fit the single-GPU adaptation category. R1 and R1-Zero also have distinct post-training histories; results must identify the exact release. |

No row is an endorsement or an activation decision. The shortlist for an eventual
experiment should be chosen only after the owner supplies the intended task,
hardware, privacy requirements, deployment terms and budget.

## Context length is not a fine-tuning budget

An advertised 128K/256K/1M inference context does not mean that a single GPU can
fine-tune at that sequence length. Context extension can require YaRN or other
settings, and may alter short-context behavior. Maximum output, reasoning output
and available training length are separate limits.

Most initial DSA examples should be evaluated at a deliberately bounded sequence
length appropriate to their statements, explanations and source. Increasing it
must be justified by measured task coverage and resource use. Truncating a
constraint or expected output to fit a sample can invalidate supervision.

The Qwen documentation distinguishes original hybrid mode from newer
thinking-only/non-thinking-only releases, and warns about serving stacks removing
reasoning fields during multi-step tool use. That is a compatibility question for
the exact pipeline; no hidden reasoning should be exposed or treated as a proof.

OpenAI's `gpt-oss` models are open-weight releases and should not be confused with
the closed/API-only category in row 20. Their official README explicitly says
the Harmony format is required. A generic chat template or flattened text-only
training record is therefore not an assumed compatible adaptation input. The
reference chat application's default context setting is not evidence of the
checkpoint's maximum supported context. Archived phi-code logs that name a
gpt-oss model are historical upstream material, not an evaluated Solver AI model.

## Hardware questions to answer before choosing

The following figures are **arithmetic lower bounds for weights only**, using
decimal GB. They are not measured VRAM requirements or fit guarantees.

| Total parameters | Two-byte weights | Four-bit payload only |
| --- | ---: | ---: |
| 4B | 8 GB | 2 GB |
| 8B | 16 GB | 4 GB |
| 14B | 28 GB | 7 GB |
| 24B | 48 GB | 12 GB |
| 32B | 64 GB | 16 GB |
| 80B | 160 GB | 40 GB |

Real use adds quantization scales/metadata, unquantized layers, activations,
attention workspaces, vocabulary/logit buffers, adapter weights/gradients,
optimizer states, allocator overhead and sometimes CPU offload. Full fine-tuning
has very different memory needs from LoRA/QLoRA. Inference fit is not training fit.

For a future **single-GPU QLoRA feasibility study**, dense 3B–8B models provide a
smaller experimental class than 24B–32B dense models or large-total-parameter MoE.
A 24 GB GPU may be a useful investigation tier for a short-context 7B/8B setup,
but this document does not guarantee it fits. GPU architecture, quantizer support,
sequence length, microbatch, checkpointing, LoRA targets/rank and trainer version
must be specified. A 16 GB device, a 24 GB device and an 80 GB device imply
different feasible comparisons. No GPU has been assumed or provisioned.

For MoE, account for **all stored experts**, routing behavior and adapter target
coverage. For hybrid attention, multimodal and state-space/Mamba architectures,
confirm training support and memory behavior instead of extrapolating from a
standard dense Transformer recipe. Some quantized releases are intended primarily
for inference and may need a different canonical artifact for adaptation.

## What good DSA adaptation data would contain

Start by defining the desired behavior: code-only solving, progressive tutoring,
debugging, or candidate ranking. They need different examples and output policies.

- Original or permissioned problem statements, constraints and public examples.
- Correct executable solutions matched to a supported compiler/runtime version.
- Concise reviewed algorithm explanations, invariants and complexity statements.
- For debugging, owned/consented code and public failure evidence, with explicit
  separation between observation and hypothesis.
- For tutoring, examples that respect spoiler level and do not reveal full code
  when a small hint was requested.
- Immutable provenance and permissions for training, evaluation, redistribution
  and commercial use, with unresolved permissions blocking use.

Do not treat a model-generated explanation as trusted supervision merely because
its program passes samples. Do not expose private grader inputs or expected
outputs to a model. Do not automatically train on private submissions. Distilled
outputs from other providers require their own permitted-use review.

The archived CodeGenerator and phi-code material remains research evidence.
Their source-code licenses do not settle dataset/problem rights. Five phi-code
dataset files are only LFS pointers; no fine-tuning plan can assume those missing
objects have been recovered. Their host execution and permissive remote-model
loading paths must not become the active training/evaluation implementation.

## How the future comparison should work

1. Define one narrow initial task and quality rubric, including Python/C++ runtime
   requirements, spoiler policy and allowed assistance mode.
2. Define separate rights-approved training, model-selection/validation and sealed
   final release-test sets with disjoint problem lineage; record exact/near-duplicate
   checks and unknown pretraining contamination. Keep the final set unopened during
   model, prompt and hyperparameter selection.
3. Establish an **untuned baseline** for each eligible candidate under documented
   prompt/template, output mode, token, candidate, test and wall-time budgets.
4. Compare compile success, finite-check correctness, failure categories, latency,
   tokens, cost and explanation quality. Separate unexecuted, skipped, failed and
   passed cases. Do not substitute source similarity for functional correctness.
5. Only after separate approval, run a small adapter experiment with fixed data,
   seed, hyperparameters, artifact revisions, hardware and hard spend ceiling.
6. Freeze the candidate, then compare tuned and untuned checkpoints on the sealed
   final release test and check for
   general instruction/tutoring regressions. Report uncertainty and negative
   outcomes; a tuning run is not itself a product improvement.
7. Keep model serving separate from the credential-free isolated judge. Execute
   generated programs through the reviewed judge, never host `exec` or a normal
   application subprocess.

Different reasoning lengths can make a nominally equal number of generations
unequal in cost. Report both quality and consumed resources. A model that performs
well on repository patching may not be the best fit for finite DSA input/output
contracts, and a model good at code-only solving may be a poor teacher.

## Official sources consulted

All sources below were accessed or attempted on **17 November 2026**. GitHub
`main` links are mutable. Publisher statements are attributed to their sources,
not independently reproduced performance measurements.

- **Q1:** [Qwen3 official README](https://raw.githubusercontent.com/QwenLM/Qwen3/main/README.md): dense/MoE family sizes, modes, release links, context/serving notes, training frameworks and Apache model-license statement.
- **Q2:** [Qwen3-Coder official README](https://raw.githubusercontent.com/QwenLM/Qwen3-Coder/main/README.md): current Coder-Next architecture, named base/instruction/quantized variants, tokenizer/tool compatibility and 256K context statement.
- **Q3:** [Legacy Qwen2.5-Coder README URL](https://raw.githubusercontent.com/QwenLM/Qwen2.5-Coder/main/README.md): currently returns the Coder-Next landing document; original checkpoint metadata remains unresolved.
- **D1:** [DeepSeek-R1 official README](https://raw.githubusercontent.com/deepseek-ai/DeepSeek-R1/main/README.md): distilled checkpoint names/base origins, full-model versus distilled distinction, usage caveats and license inheritance notes.
- **D2:** [DeepSeek-Coder-V2 official README](https://raw.githubusercontent.com/deepseek-ai/DeepSeek-Coder-V2/main/README.md): total/active parameter sizes, architecture/context and separate code/model licenses.
- **P1:** [Microsoft Phi family overview](https://raw.githubusercontent.com/microsoft/PhiCookBook/main/md/01.Introduction/01/01.PhiFamily.md): checkpoint links and stated sizes; contains the noted reasoning-size inconsistency.
- **P2:** [Microsoft Phi reasoning recipe](https://raw.githubusercontent.com/microsoft/PhiCookBook/main/md/02.Application/03.AdvancedReasoning/Phi4/AdvancedResoningPhi4mini/README.md): names 3.8B mini reasoning and 14B reasoning, with generation-format examples. A cookbook recipe is not a pinned model card.
- **G1:** [Official Gemma PyTorch README](https://raw.githubusercontent.com/google/gemma_pytorch/main/README.md): Gemma 3/2/CodeGemma implementation support and size/packaging information.
- **G2:** [Current DeepMind Gemma README](https://raw.githubusercontent.com/google-deepmind/gemma/main/README.md): includes a Gemma 4 E4B implementation example and links its official card. Its [library license](https://raw.githubusercontent.com/google-deepmind/gemma/main/LICENSE) must not be generalized to checkpoint weights.
- **L1:** [Meta Llama model index](https://raw.githubusercontent.com/meta-llama/llama-models/main/README.md): release families, size/context table and per-release model card/license links.
- **L2:** [Actual Llama 3.1 model card](https://raw.githubusercontent.com/meta-llama/llama-models/main/models/llama3_1/MODEL_CARD.md): architecture, sizes, use conditions and evaluation caveats.
- **L3:** [Llama 3.1 Community License](https://raw.githubusercontent.com/meta-llama/llama-models/main/models/llama3_1/LICENSE): custom terms including redistribution/attribution and additional commercial conditions.
- **M1:** [Mistral official inference README](https://raw.githubusercontent.com/mistralai/mistral-inference/main/README.md): named distributions, per-artifact license exceptions, NeMo and Small 3.1 links.
- **M2:** [Mistral official fine-tune README](https://raw.githubusercontent.com/mistralai/mistral-finetune/main/README.md): archived-maintenance notice, training examples and NeMo vocabulary/loss-memory warning.
- **S1:** [StarCoder2 official README](https://raw.githubusercontent.com/bigcode-project/starcoder2/main/README.md): size/context/attention information and LoRA/4-bit example. Its [GitHub license](https://raw.githubusercontent.com/bigcode-project/starcoder2/main/LICENSE) is a source-code license, not proof of weight terms.
- **I1:** [IBM Granite Code official README](https://raw.githubusercontent.com/ibm-granite/granite-code-models/main/README.md): model variants, exact context-tagged IDs, training discussion and Apache model-license statement.
- **O1:** [OpenAI gpt-oss official README](https://raw.githubusercontent.com/openai/gpt-oss/main/README.md): total/active parameter counts, Harmony requirement, reasoning-effort choices, fine-tunability and qualified MXFP4 inference-memory claims. No inference or fine-tuning example was executed.
- **O2:** [OpenAI gpt-oss repository license](https://raw.githubusercontent.com/openai/gpt-oss/main/LICENSE): Apache 2.0 text, considered together with the README's explicit model-release licensing statement. A guessed `docs/model-card.md` URL returned 404; it is not treated as a retrieved model card.

Direct model-card/config requests to `huggingface.co` were blocked. These links
remain required follow-up evidence, rather than claimed successful retrievals:
[Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B),
[Qwen2.5-Coder-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct),
[Qwen3-Coder-30B-A3B-Instruct](https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct),
and the corresponding official publisher repositories for every shortlisted row.

## Future decision checklist

- [ ] Owner identifies the primary task: tutoring, debugging, code solving or research.
- [ ] GPU/CPU/RAM, available VRAM, maximum sequence length, throughput and spend limits are known.
- [ ] Exact checkpoint, base/instruction variant, weight format, tokenizer/chat template and immutable revision are verified from official metadata.
- [ ] Weight, base-model, dataset, provider-output and redistribution terms are independently reviewed.
- [ ] The training framework supports the exact architecture/quantization without arbitrary unreviewed remote code.
- [ ] Public-only context, source-sharing consent, retention, quotas and isolation boundaries are agreed.
- [ ] Rights-approved train/validation/test manifests are complete and disjoint; missing LFS content is not assumed available.
- [ ] Untuned baseline and comparable evaluation budgets are defined before adapter training.
- [ ] A separately approved small experiment has a hard resource ceiling, rollback path and negative-result reporting policy.
- [ ] Promotion depends on measured benefit and acceptable regressions; no candidate is selected by this document.
