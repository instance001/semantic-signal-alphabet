# Bucket Generation Process

Semantic Signal Alphabet is built around a simple generation flow.

The system takes a source set, applies a fixed bucket limit, asks the target model to build the most useful semantic partition it can within that limit, and saves the result as a frozen artifact.

The point of the process is not to force total coverage.
The point is to create a reusable semantic alphabet that is honest about its limits.

## Inputs

A generation run begins with a defined source set.

That source set may be:
- a word list
- a domain vocabulary
- a project map
- a compiler error list
- a file or document taxonomy
- a concept inventory
- any other structured set of items to be compressed semantically

The source set should be treated as explicit input rather than vague background context. The more clearly the source domain is defined, the more interpretable the resulting alphabet will be.

## Bucket Count Selection

The next input is the target bucket count.

This is one of the most important decisions in the process because the bucket count defines the available bandwidth of the alphabet.

The bucket count should be treated as application-defined. The tool or model should not casually invent it.

A lower bucket count creates a broader and more compressed alphabet.
A higher bucket count allows finer semantic distinction.

The bucket count should be chosen based on the real constraints of the use case:
- signal quality
- channel resolution
- task complexity
- desired breadth versus precision
- whether the alphabet is meant for coarse narrowing or finer routing

The system should not pretend to have more usable resolution than the task can realistically support.

This creates a clean division of labor:
- the application defines how many buckets are available
- the model defines how to sort the source material within that fixed budget

## Target Model Selection

The model chosen for generation matters because the system is intentionally model-native.

The target model is not just a generic helper. It is part of the alphabet definition.

The bucket map should therefore be treated as model-specific. If a different model will be used at runtime, that different model should have its own bucket generation pass rather than inheriting another model's semantic partition as though it were universal.

Once the bucket count has been set by the application, the model's job is to determine the semantic shape of the active buckets, not the number of buckets themselves.

A bucket map should therefore always record:
- the model used
- the prompt version used
- the source input used
- the bucket count used

A generated alphabet should always be understood as linked to the model and generation conditions that produced it.

This also means bucket generation should happen before exposing the runtime system to user-specific interaction logs. First generate the alphabet from the model's own native logic. Then allow later runtime adaptation to user patterns.

## Generation Prompt Principle

The generation prompt should be simple, explicit, and centered on coverage within constraint.

A standard instruction principle for the system is:

> Sort these words/items into X amount of buckets with as diverse linguistic or domain coverage as possible. Full coverage is not expected. Prioritize broad, useful semantic coverage within the bucket number limit. Place items that do not fit cleanly into UNASSIGNED.

This instruction matters because it tells the model what to optimize for:
- exact bucket count
- broad usefulness
- semantic diversity
- honest overflow instead of forced fit

The goal is not exhaustive categorization.
The goal is useful compression under a hard bandwidth limit.

## Coverage Goals

The generation process should prioritize:
- broad semantic usefulness
- internal coherence
- useful spread across the source domain
- honest handling of non-fitting material

It should not prioritize:
- forced completeness
- cosmetic neatness
- arbitrary balancing for its own sake
- pretending every item belongs somewhere cleanly

A strong alphabet may leave many items unassigned if that is the truthful result of the compression boundary.

## Bucket Shape

Each generated bucket should ideally contain:
- a short label
- a plain-language summary
- anchor items that help define the bucket's center of gravity
- assigned items that reasonably fit the region

This makes the bucket map easier to inspect, version, compare, and reuse later.

The labels do not need to be perfect scientific names. They need to be useful handles for understanding what semantic region the model has created.

## UNASSIGNED Handling

Items that do not fit cleanly should remain `UNASSIGNED`.

This should be treated as a normal part of the generation output.

The `UNASSIGNED` set may later be used for:
- edge-case review
- alternate alphabet generation
- bucket splitting decisions
- fallback logic in downstream systems
- data collection about where the current map is weak

The generation process should preserve this material, not hide it.

## Model Change Procedure

If the system changes from one model to another, the alphabet should be regenerated with the new model before any historical user logs are applied.

The intended order is:
1. choose the target model
2. generate a fresh bucket map with that model
3. freeze the new model-specific artifact
4. only then expose runtime layers to prior user logs or behavioral history

This preserves the core premise of the framework: the bucket structure should come from the target model's own semantic logic, not from a preloaded user-history bias.

## Freezing The Output

Once an alphabet has been generated, it should be saved as a frozen artifact.

This matters because downstream systems need a stable semantic reference.

If the bucket map changes silently over time, then adapters and interpreters may no longer be operating against the same meaning structure they were built around.

A new generation run should create a new artifact, not overwrite the meaning of an old one.

## Versioning Requirements

Every saved bucket map should include enough metadata to explain how it was produced.

At minimum, that should include:
- model name
- prompt version
- bucket count
- source dataset or manifest
- creation timestamp
- bucket definitions
- assigned items
- unassigned items

Additional metadata may be added later, but those fields form the minimum traceability layer.

## Design Rule

Keep the generation process simple, explicit, and auditable.

Choose a source set.
Choose a bucket count.
Use the target model to build the best partition it can.
Preserve uncertainty.
Freeze the result.

That is the core generation flow of Semantic Signal Alphabet.
