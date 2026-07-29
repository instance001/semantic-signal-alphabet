# Generator Tool Specification

This document defines the first implementation target for Semantic Signal Alphabet.

The goal is not to build a full platform. The goal is to define the smallest useful tool that can generate a frozen bucket map artifact from a source set, a bucket count, and a target model configuration.

This is a docs-only specification for the first tooling pass.

## Purpose

The generator tool exists to turn the repository's core idea into a repeatable artifact workflow.

Given:
- a source manifest or source item list
- a target bucket count
- a target model
- a prompt version
- optional domain constraints or notes

the tool should produce:
- a frozen bucket map artifact
- complete generation metadata
- a clear record of unassigned items

The tool is part of the core framework. It is not a downstream adapter.

The central rule is:
- the application defines the bucket count
- the model defines the sorting within that count

The second rule is:
- alphabets are model-specific
- user-log adaptation happens after bucket generation, not before it

## Non-Goals For The First Version

The first version should not try to solve every future need.

It does not need:
- live runtime interpretation
- user personalization
- consensus generation across many runs
- automatic bucket quality scoring
- model comparison dashboards
- BCI integration
- code-routing integration
- UI-heavy workflows

Those may come later. The first tool only needs to generate structured artifacts cleanly and consistently.

## Core Workflow

The first generator tool should follow a simple sequence:

1. Load a source manifest or source item list.
2. Validate the source input shape.
3. Accept a target bucket count.
4. Accept a target model identifier and prompt version.
5. Build the generation prompt using the repository's standard prompt principle.
6. Request a bucketed semantic partition from the model.
7. Normalize the response into the bucket map artifact structure.
8. Preserve items that do not fit as `UNASSIGNED`.
9. Save the artifact with metadata and timestamp.
10. Refuse to mutate existing artifacts silently.

This workflow should stay explicit and inspectable.

## Inputs

The minimum input set for version one should be:
- `source`
- `bucket_count`
- `model`
- `prompt_version`

Optional inputs may include:
- `domain_constraints`
- `notes`
- `artifact_id`
- `output_path`

### Source Input

The tool should accept either:
- a path to a source manifest JSON file
- a direct list of source items

If a direct list is used, the tool should still normalize it into source-manifest-like metadata in the saved artifact.

### Bucket Count

The tool should require an explicit positive integer bucket count.

It should not infer this automatically in version one.

Bucket count is a design input, not a convenience default.

More specifically, bucket count should be treated as application-owned input. If a downstream use case can only support six distinct states, then the tool should generate six active buckets, not a model-chosen alternative.

### Model

The tool should require an explicit model identifier.

Even if a default model is later supported, the actual saved artifact must record the exact model name used during generation.

The tool should assume that the generated alphabet belongs to that model. If a different model is later used, a new generation pass should be treated as necessary rather than optional.

### Prompt Version

The tool should require a prompt version string.

This keeps generated artifacts traceable and makes future prompt refinements safe.

## Prompt Contract

The generator tool should not rely on hidden prompt behavior.

It should use a prompt contract aligned with the repository docs. A first-pass instruction can be based on this principle:

> Sort these words/items into X amount of buckets with as diverse linguistic or domain coverage as possible. Full coverage is not expected. Prioritize broad, useful semantic coverage within the bucket number limit. Place items that do not fit cleanly into UNASSIGNED.

The prompt should also instruct the model to return structured output suitable for normalization into the bucket map schema.

The generation step should be isolated from user-history bias. Historical logs, prior user interaction traces, or other adaptation data should not be injected into the prompt context for the initial bucket-generation pass.

At minimum, the returned content should contain:
- exactly `bucket_count` active buckets
- a label for each bucket
- a summary for each bucket
- anchor items for each bucket
- assigned items for each bucket
- an `UNASSIGNED` list

## Output Artifact

The primary output is a bucket map artifact matching [bucket_map.schema.json](../schemas/bucket_map.schema.json).

The first tool should always produce:
- `schema_version`
- `artifact_type`
- `model`
- `prompt_version`
- `bucket_count`
- `source_manifest`
- `created_at`
- `buckets`
- `unassigned_items`

Optional metadata such as `artifact_id` and `notes` should be included when available.

The saved artifact is the product. Console output is secondary.

## Response Normalization

The tool should expect model output to need normalization.

The normalization layer should:
- verify the correct number of active buckets exists
- coerce labels and summaries into strings
- ensure anchor and assigned items are arrays of item objects
- collect unresolved or rejected items into `unassigned_items`
- fail clearly if the response is too malformed to trust

If the model returns more or fewer active buckets than requested, the tool should treat that as an error unless an explicit recovery mode exists in a later version.

Version one should prefer strictness over hidden repair.

The generator is not responsible for deciding the bucket number. Its job is to enforce the application-defined bucket count and let the model decide the semantic arrangement inside it.

It should also preserve the model-native step by ensuring that bucket generation happens before any later log-based adaptation layers are applied.

## Validation Rules

Before saving, the tool should validate:
- source input exists and is non-empty
- `bucket_count` is a positive integer
- the normalized output contains exactly `bucket_count` buckets
- required fields are present
- the artifact matches the bucket map schema

If validation fails, the tool should fail clearly and leave existing saved artifacts untouched.

## File Behavior

The tool should be conservative about file writes.

Version one should:
- create new artifacts rather than silently overwrite old ones
- allow explicit output paths
- default to a predictable output location if none is provided
- keep raw input and output traceability where practical

Possible default output pattern:

`artifacts/<source_id>/<model>/<bucket_count>/<timestamp>.json`

This exact layout can change, but the principle should remain:
artifacts should be easy to trace by source, model, and bucket count.

## Error Handling

The first generator should fail in understandable ways.

It should surface errors such as:
- missing source input
- empty source list
- invalid bucket count
- missing model identifier
- malformed model response
- wrong number of returned buckets
- schema validation failure
- output path conflicts

Errors should explain what failed and where in the process it failed.

## Traceability

Traceability is a core requirement, not a nice-to-have.

Every generated artifact should make it possible to answer:
- what source was used
- what model was used
- what prompt version was used
- what bucket count was used
- when the artifact was created

If a later runtime system uses historical logs to adapt to a specific user, that should be treated as downstream behavior layered on top of the artifact, not as part of the bucket-generation truth itself.

If later generations differ, those differences should produce new artifacts rather than silent edits to old ones.

## Suggested Interface Shape

The exact implementation language can be decided later, but the first tool should likely support a simple command shape such as:

```text
ssa-generate --source path/to/source_manifest.json --bucket-count 8 --model MODEL_NAME --prompt-version v1 --output path/to/artifact.json
```

Or, if implemented as a script inside the repo:

```text
python tools/generate_bucket_map.py --source ... --bucket-count ... --model ... --prompt-version ...
```

The interface should stay narrow and boring in version one.

## Suggested Internal Components

Even a small implementation will benefit from clear separation of responsibilities.

The first tool will likely need:
- input loader
- source manifest normalizer
- prompt builder
- model client wrapper
- response normalizer
- schema validator
- artifact writer

These do not need to be large modules at first. They just need to map cleanly to the workflow.

## Open Design Questions

These questions do not block version one, but they should remain visible:

- Should source items always be stored inline, or sometimes only by manifest reference?
- Should raw model output be saved alongside normalized artifacts?
- Should reruns with the same inputs require explicit overwrite or always create a new artifact?
- Should later versions support repeated-run consensus generation?
- Should bucket labels remain model-authored, or should optional post-normalization label cleanup be allowed?
- Should later tooling explicitly separate "generation context" from "runtime adaptation context" in saved metadata?

Version one does not need perfect answers to all of these questions.

## Acceptance Criteria For Version One

The first generator tool is complete when it can:
- load a source input
- accept an explicit bucket count
- use an explicit model and prompt version
- produce exactly the requested number of buckets
- preserve unassigned items
- save a valid bucket map artifact
- validate its output before writing
- avoid silent mutation of prior artifacts

That is enough to move the project from pure documentation into artifact generation without overbuilding the system.
