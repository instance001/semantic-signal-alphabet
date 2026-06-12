# Model Specificity And Migration

Semantic Signal Alphabet is model-native by design.

That means a bucket map is not just tied to a source set and a bucket count. It is also tied to the specific model that generated it.

This document explains what that means in practice, especially when a system changes models or begins adapting to a particular user's habits over time.

## Bucket Maps Are Model-Specific

A bucket map should be treated as a model-specific artifact.

The model that will later interpret, rank, narrow, or otherwise work with an alphabet should be the same model used to generate that alphabet in the first place.

This follows directly from the core premise of the project:
- the application defines the bucket number
- the target model defines the sorting within that number

If the sorting is meant to be model-native, then the resulting alphabet belongs to the model that created it.

## Why Model Specificity Matters

Different models may have different:
- semantic priors
- salience patterns
- clustering tendencies
- vocabulary associations
- reasoning habits

Two models can receive the same source set and the same bucket count and still produce different but valid alphabets.

That is expected.

Trying to treat one model's bucket map as universally portable across all other models weakens the central logic of the framework. It risks forcing a new model to reason inside a partition that was not generated from its own native tendencies.

## The Correct Order Of Operations

The order of operations matters.

When setting up a system for a specific model, the intended sequence is:

1. choose the application or adapter
2. determine the application-defined bucket count
3. choose the target model
4. generate the bucket map with that model
5. freeze the model-specific artifact
6. only then allow downstream runtime systems to learn from user history, logs, or interaction patterns

This preserves the clean separation between:
- model-native alphabet generation
- user-specific runtime adaptation

## User Logs Come After Bucket Generation

A runtime system may absolutely benefit from user history.

Over time, interaction logs may help a downstream interpreter:
- rank likely meanings more effectively
- narrow candidates faster
- recognize repeated user habits
- pre-seed common preferences or patterns
- improve clarification behavior

That is useful.

But that should happen after the bucket map has already been generated.

The initial alphabet-generation pass should not be pre-biased by old user logs if the goal is to let the target model produce its own native semantic partition.

In other words:
- first let the model define the semantic map
- then let runtime behavior adapt to the user inside that map

## Why Logs Should Not Lead Generation

If historical logs are injected before bucket generation, the resulting partition may become a mixture of:
- the model's semantic priors
- the old user's habits
- the assumptions of a previous runtime context
- possibly even the behavior of a different model

That can blur the very thing the framework is trying to preserve.

Semantic Signal Alphabet is strongest when the alphabet begins as a clean model-native artifact. Personalization should be layered on afterward.

## Model Migration Rule

If the system changes from one model to another, a fresh bucket generation pass should be done with the new model before historical logs are introduced.

This should be treated as a normal migration rule, not an unusual edge case.

The new order should be:

1. switch to the new target model
2. generate a new bucket map using that model alone
3. freeze the new model-specific alphabet
4. only then expose the runtime layer to old user logs for adaptation

This allows the new model to sort according to its own native logic first, while still preserving the value of historical user patterns later.

## Example: Communication System Migration

Imagine a communication adapter built around a six-bucket signal system.

The adapter originally uses `Model-A`, and over time it accumulates user interaction logs showing:
- common word preferences
- common clarification paths
- common bucket combinations
- recurring habits in how one user expresses intent

If the adapter later moves to `Model-B`, it should not immediately use those old logs to shape bucket generation.

Instead it should:
- keep the six-bucket count because the application still defines the bandwidth
- let `Model-B` generate its own six-bucket map
- freeze that new map
- then let the runtime system use old logs to help `Model-B` adapt to the user's established patterns

This keeps the bandwidth rule and the model-native rule intact at the same time.

## What Stays Stable And What Can Adapt

The framework works best when these responsibilities stay separate:

Stable:
- source set definition
- application-defined bucket count
- chosen target model for the artifact
- frozen bucket map produced by that model

Adaptive:
- ranking behavior
- clarification loops
- user-specific preference learning
- topic narrowing
- runtime use of historical logs

This separation allows personalization without corrupting the core artifact-generation step.

## Metadata Implications

Because model specificity matters, saved artifacts should make it easy to identify:
- the exact model used for generation
- the prompt version used
- the bucket count used
- the source set used
- when the artifact was created

Later systems may also benefit from separately tracking:
- the runtime model in use
- whether runtime adaptation logs were applied
- what user-history source was used for adaptation

Those runtime details should remain distinct from the bucket-generation record.

## Design Rule

Treat alphabets as model-specific.

When models change, regenerate first and adapt second.

Do not let user-history bias shape bucket generation before the target model has had a chance to define its own semantic partition.
