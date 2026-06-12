# BCI Triangulation Runtime

This document describes a possible runtime shape for a brain-computer interface adapter built on top of Semantic Signal Alphabet.

It is not a claim of direct thought decoding. It is a description of a probabilistic narrowing workflow that uses coarse bucket activations to help an LLM rank likely meanings inside a constrained semantic space.

It is also not a fixed runtime prescription. Different users, devices, vocabularies, and signal constraints may require very different values while still following the same basic workflow.

## Core Idea

The BCI adapter should be understood as a triangulation system.

The signal layer does not need to directly decode an exact word from raw brain activity. It only needs to provide enough stable bucket activations for the target model to narrow the likely candidate space.

The high-level logic is:
- the application defines how many signal patterns are actually usable
- the target model generates a bucket map for that exact count
- the runtime observes which buckets appear to activate
- the model ranks likely candidates inside those active semantic regions
- clarification and repetition help converge on the user's intended meaning

This is a probabilistic interpretation system, not a one-shot decoder.

## Runtime Stages

At a high level, the BCI adapter may operate in stages:

1. source vocabulary selection
2. bucket-map generation
3. signal calibration
4. live bucket-hit observation
5. candidate ranking
6. clarification loop
7. user-history adaptation

Each stage supports the next.

## Stage 1: Source Vocabulary Selection

The first step is deciding what source vocabulary the adapter should use.

This does not need to be the entire English language in an exhaustive sense. A practical dictionary-scale list or common-word list may be enough for many experiments.

The source set may be:
- a broad general English vocabulary
- a narrower communication vocabulary
- a domain-specific word set
- a topic-limited active vocabulary

The narrower the source window, the easier the runtime's ranking problem becomes.

This is user-configurable. One user may choose 1,000 scoped words for faster convergence, while another may choose 100,000 broader words and accept slower narrowing.

## Stage 2: Bucket-Map Generation

Once the source vocabulary and signal limits are known, the target model should generate the bucket map.

The rules remain the same:
- the application defines the bucket count
- the model defines the sorting inside that count
- `UNASSIGNED` captures words that do not fit cleanly

If the BCI setup can only support six stable signal distinctions, then the alphabet should be generated for six active buckets, plus `UNASSIGNED` as a separate overflow set.

The resulting bucket map becomes the stable semantic reference for the runtime.

That number is not a framework default. It is an application-specific value that should be set by the user's actual hardware and calibration limits. Another setup may only support two buckets, while another may support many more.

## Stage 3: Signal Calibration

Before live interpretation, the adapter likely needs a calibration phase.

In practice, this may involve asking the user to focus on or imagine a known calibration cue associated with each bucket channel. The details depend on the signal system, but the purpose is the same:

- establish which detectable signal patterns correspond to which active bucket channels
- estimate how stable those patterns are
- measure ambiguity and overlap

This is where the adapter learns how the user's signal layer maps to the bucket structure.

The calibration cues themselves do not need to be final words. They can be prompts, focus tasks, or representative semantic anchors.

## Stage 4: Live Bucket-Hit Observation

Once calibration exists, the runtime can observe incoming signal activity and estimate which buckets appear most likely to be active.

Useful runtime information may include:
- which buckets fired
- the order they fired in
- how strongly they appeared to activate
- whether the same bucket repeated
- whether the pattern was noisy or stable

At this stage, the system still does not know the exact intended word or meaning. It only has a rough semantic region or sequence of regions.

That is enough to begin narrowing.

## Stage 5: Candidate Ranking

The target model can now use the bucket map plus runtime hit data to rank likely candidates.

For example, if buckets `2`, `4`, and `5` appear to activate in a particular order, the model can search within the words or concepts associated with those regions and ask:

- what candidates best fit this bucket combination?
- what candidates best fit this order?
- what candidates are most likely for this user's past behavior?
- what candidates are most likely in the current topic scope?

This is where Semantic Signal Alphabet becomes useful as a bounded search space.

The model is no longer searching all possible English words equally. It is searching inside a constrained semantic region defined by the bucket artifact and the observed activations.

## Stage 6: Clarification Loop

Because the system is probabilistic, clarification should be treated as normal.

A simple runtime may use:
- yes/no confirmation
- multiple-choice narrowing
- repeated attempts
- re-prompted focus
- additional bucket observations

For example:
- "Did you mean X?"
- if no, "Did you mean Y?"
- if no, narrow again based on the next best-ranked candidates

This does not make the system weak. It is part of how the adapter turns coarse signals into useful interpretation.

## Stage 7: User-History Adaptation

Over time, the runtime should become more predictive for a specific user.

Logs and interaction history may help the runtime learn:
- common intended words
- common topics
- common bucket combinations
- common confirmation patterns
- preferred vocabularies
- recurring semantic habits

This is similar to how long-running chat interactions can become better at predicting what a user is likely to mean next.

The important rule is timing:
- do not use old logs to shape the initial bucket generation step
- do use logs later to improve runtime ranking and clarification

Generation stays model-native.
Adaptation becomes user-native over time.

## Broad Mode And Scoped Mode

The adapter may operate in at least two useful modes.

### Broad Mode

Broad mode uses a larger vocabulary and less restrictive topic scope.

Benefits:
- more general-purpose use
- broader communication range

Tradeoffs:
- slower convergence
- more ambiguity
- more clarification steps
- more runtime data needed before strong predictions emerge

### Scoped Mode

Scoped mode uses a narrower active vocabulary or topic window.

Examples:
- emotions only
- household requests only
- project-specific vocabulary only
- people-and-actions only

Benefits:
- faster narrowing
- stronger ranking
- less ambiguity
- fewer required runs

Tradeoffs:
- less general range
- requires explicit context selection or domain switching

Both modes are valid. Scoped mode may be especially useful in early practical systems.

## Why UNASSIGNED Still Matters

Some words or concepts may not fit the active bucket map cleanly, especially in a low-bucket-count BCI system.

Those items should remain in `UNASSIGNED`.

In the BCI runtime, `UNASSIGNED` may help by:
- identifying vocabulary that is too awkward for the current alphabet
- signaling when the active scope should be narrowed
- acting as a reminder that some intended concepts may need alternate handling
- contributing edge-case data for later bucket-map refinement

It is better to preserve that uncertainty than to force weak placements.

## Model Change Procedure

If the adapter changes models, it should not simply reuse the old model's alphabet as though nothing changed.

The correct procedure is:
1. keep the application-defined bucket count if the signal layer is unchanged
2. choose the new target model
3. generate a fresh bucket map with that model
4. freeze the new model-specific artifact
5. only then reintroduce historical logs to help runtime adaptation

This preserves the model-native logic of the semantic partition while still allowing long-term user-history value to carry forward afterward.

## Practical Summary

The BCI adapter should be understood as:
- a coarse-bandwidth semantic interface
- a triangulation system for probabilistic narrowing
- a runtime that gets better with user-specific history
- a workflow that benefits from scoped vocabularies when possible
- a downstream application of the core Semantic Signal Alphabet framework

It is not direct brain reading.
It is not a guarantee of exact immediate decoding.

It is a structured way to let a model use limited bucket activations to narrow likely meaning inside a constrained semantic space.
