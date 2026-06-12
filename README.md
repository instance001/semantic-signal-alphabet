# Semantic Signal Alphabet

_A model-native semantic compression framework._

Semantic Signal Alphabet is a standardized, domain-agnostic system for generating low-bandwidth, model-native semantic alphabets from vocabularies, datasets, and other source domains.

The bucket count is the bandwidth. The model supplies the compression logic.

In this project, an "alphabet" means a constrained, reusable meaning system. It is not a literal character encoding. It is a bounded semantic map that an interpreter can reuse later.

Instead of forcing an LLM to work inside a human-authored taxonomy, Semantic Signal Alphabet asks the target model to sort a source set into a fixed number of broad semantic buckets with as much useful coverage as possible. The result is a frozen bucket map that can later be reused as an interpretation scaffold for communication, routing, classification, and semantic compression across many domains.

## What This Project Is

This repository defines the core alphabet-generation framework, not any single downstream application.

A source set might be:
- English words
- domain vocabulary
- compiler errors
- code issues
- project artifacts
- file categories
- mathematical concepts
- business terms
- any other set of items that needs to be compressed into a smaller semantic space

The system takes that source set, applies a fixed bucket budget, and asks an LLM to create the most useful semantic partition it can within that limit.

This repository standardizes the generation process and the saved artifact format. It does not claim there is one universal alphabet for all models, domains, or use cases.

## Core Idea: Bucket Count Is Bandwidth

The central principle of Semantic Signal Alphabet is simple:

`bucket count = available bandwidth`

In practical terms:
- the application defines the bucket number
- the LLM defines the sorting within that number

If a system can only reliably distinguish a small number of states, then the resulting alphabet must be coarse. If a system can support more distinguishable states, the alphabet can become more granular.

Examples:
- `2` buckets may only support broad binary distinctions
- `6` buckets may support coarse semantic regions in a low-resolution signal system
- `16`, `32`, or `64+` buckets may support finer domain partitioning for code, projects, or technical reasoning

The goal is not maximum granularity at all times. The goal is the most useful semantic coverage possible within the real bucket limit of the channel, task, or system.

This is the core mechanism of the framework. The application or channel sets the hard bucket budget. The target model is then responsible for deciding how to use that limited semantic space as effectively as possible.

## Why Model-Native Sorting Matters

Many systems begin with human-designed categories and ask the model to fit incoming material into them. Semantic Signal Alphabet takes the opposite approach.

Instead of saying, "here are our buckets, work within them," this system says, "here is the bandwidth limit, build the best bucket map you can."

The design hypothesis is that the target model may reason more naturally over a bucket system that reflects its own semantic priors than over one imposed externally. That may reduce semantic mismatch and lower the amount of reasoning spent reconciling arbitrary human bucket boundaries.

This is not a claim of objective truth. Different models may generate different valid alphabets from the same source material. Even the same model may produce slightly different valid outputs across runs. The framework does not require one perfect universal result. It requires a useful, versioned, reusable semantic map.

This also means alphabets should be treated as model-specific artifacts. The model that will later interpret or work with an alphabet should be the model used to generate that alphabet in the first place.

## Not Just Classification

Semantic Signal Alphabet is not just a tagging or clustering scheme.

It is a system for bandwidth-constrained semantic compression. The purpose of the generated alphabet is not merely to organize a dataset once, but to create a reusable interpretation scaffold that can support later reasoning, routing, interaction, or communication.

## Granularity Depends On Use

Not every use case needs the same resolution.

Some applications are naturally coarse because the underlying channel is coarse. Others can support a much finer semantic partition.

For example, a low-resolution brain-computer interface may only be able to distinguish a very small number of signal patterns. In that case, the generated alphabet may contain only a few broad semantic buckets, each holding many candidate words or meanings. Those bucket hits may still be useful because they narrow the search space enough for iterative interpretation, clarification, ranking, or user-guided narrowing over time.

If a BCI application can only support six distinct signal patterns, then the active alphabet should be generated for six buckets. That bucket number is set by the application constraint, not by model preference. The model's role is to decide how best to sort the source material inside that fixed six-bucket budget, while still preserving `UNASSIGNED` for non-fitting items.

A higher-resolution domain such as code analysis, compiler error routing, or project structure may support more buckets with fewer items in each. That allows more precise narrowing and more targeted interpretation.

The system is designed to support both cases. Broad semantic continents are valid. Narrow semantic regions are also valid. The right answer depends on the real bandwidth of the problem.

## How The System Works

1. Load a source vocabulary, dataset, or domain item set.
2. Set the target bucket count based on the application or channel constraint.
3. Ask the model to sort the source into exactly that many semantic buckets with maximum useful coverage.
4. Allow non-fitting items to remain `UNASSIGNED`.
5. Save the result as a frozen bucket map artifact.
6. Reuse that artifact in downstream systems, interpreters, or adapters.

The alphabet artifact stays fixed once generated. Downstream runtime systems may still adapt how they rank, clarify, or narrow candidates while using that frozen map.

If a runtime system later uses interaction logs or user history, that exposure should happen after the bucket map has been generated. The initial bucket generation step should remain tied to the target model's own native logic rather than being shaped by prior user logs.

A generation prompt will generally follow this principle:

> Sort these words/items into X amount of buckets with as diverse linguistic or domain coverage as possible. Full coverage is not expected. Prioritize broad, useful semantic coverage within the bucket number limit. Place items that do not fit cleanly into UNASSIGNED.

The key split of responsibility is:
- the application decides how many buckets are available
- the model decides how to populate those buckets

## The Bucket Map Artifact

The core output of this system is the bucket map.

A bucket map is a frozen, versioned artifact that records how a specific model partitioned a specific source set under a specific bucket constraint.

A bucket map should include:
- model name
- prompt version
- bucket count
- source dataset or source manifest
- creation timestamp
- bucket labels
- bucket summaries
- anchor items or anchor words
- assigned items
- unassigned items

Once generated, the bucket map should be treated as stable for downstream use. New alphabets can be generated later, but each saved alphabet should remain frozen so that interpreters and adapters are working from a consistent semantic reference.

This distinction matters:
- the alphabet artifact is frozen
- the runtime logic built on top of it may still adapt over time

If the underlying model changes, a new bucket map should be generated with the new model before any old user logs are introduced. Once that new model-native alphabet exists, historical logs may then be used to help the runtime system adapt to the user's established habits.

## Why `UNASSIGNED` Exists

`UNASSIGNED` is a feature, not a failure.

Full coverage should not be forced. If an item does not fit cleanly into the available bucket structure, forcing it into a weak match creates false certainty and degrades the usefulness of the alphabet.

`UNASSIGNED` serves several purposes:
- honest overflow for items that do not belong cleanly anywhere
- evidence that the current alphabet may be too coarse for some material
- a refinement queue for future bucket splitting or alternate alphabet generation
- an ambiguity set or fallback class for downstream systems handling uncertain cases
- a source of edge-case data collection

In some applications, `UNASSIGNED` may become operationally useful in its own right as an uncertainty reservoir rather than a discard pile.

## Adapters Are Not The Core

This repository is about the semantic alphabet framework itself.

Downstream tools may eventually use these alphabets for:
- low-bandwidth communication systems
- brainwave or BCI-style interpretation
- gesture interfaces
- smart-home control
- code repair routing
- compiler error classification
- project and repository compression
- file or document sorting
- domain-specific reasoning workflows

Those are adapters built on top of the core system. They are not the definition of the core repo.

The core repo owns the generation logic, artifact structure, and design principles for semantic alphabets. Adapters consume those artifacts in application-specific ways.

## Potential Applications

Semantic Signal Alphabet is designed to be general-purpose.

Possible applications include:
- low-bandwidth signal interpretation
- accessibility-style communication systems
- project and repository analysis
- file and document routing
- compiler error grouping
- code repair routing
- memory-saving context compression for LLM workflows
- domain maps for mathematics, physics, business, writing, or software engineering
- narrow topic alphabets for specialized interpreters

The framework is not limited to words. Any structured source domain that benefits from semantic compression may be a candidate.

## Scope And Safety

Semantic Signal Alphabet is not a medical project.

It is not a claim of full thought decoding.
It is not a brain-reading product.
It is not tied to one hardware stack or one signal source.
It does not claim that one bucket map is the single objectively correct representation of a domain.

Some downstream applications may eventually involve uncertain, speculative, or low-resolution signals. The core repository should be understood as an architectural and semantic compression framework, not as proof of any sensational decoding capability.

## Repository Structure

This repository is docs-first in its initial phase.

Current structure:
- `docs/` for premise, architecture, design principles, and boundaries
- `docs/09_generator_tool_spec.md` for the first implementation target
- `docs/10_model_specificity_and_migration.md` for model-specific alphabet generation and model-change procedure
- `schemas/` for bucket map and source manifest formats
- `examples/` for example generated alphabets
- future adapter folders only after the core system is clearly documented

## Project Status

This repository is currently focused on explanation, architecture, schemas, and example artifact structure.

The first pass is complete when the repo clearly explains:
- what Semantic Signal Alphabet is
- why bucket count acts as bandwidth
- why model-native sorting matters
- why `UNASSIGNED` is important
- why adapters are downstream of the core system
- how bucket maps should be structured and frozen

No production implementation is included in this initial phase.
