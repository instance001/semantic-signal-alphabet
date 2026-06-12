# Bucket Count Is Bandwidth

The governing principle of Semantic Signal Alphabet is that the number of buckets is not a cosmetic setting. It is the available bandwidth of the system.

A bucket count defines how many distinguishable semantic regions the alphabet is allowed to contain.

The system should not ask for more resolution than the channel, task, or interpreter can realistically support.

This means:
- the application defines the bucket number
- the model defines the sorting within that number

## Bandwidth Before Granularity

The first question is not "how detailed should the alphabet be?"

The first question is:

"How many distinct semantic states can this system reliably make use of?"

That answer determines the bucket count.

The bucket count should come from the application reality, not from the model improvising its preferred level of detail.

If the answer is small, the alphabet must stay broad.
If the answer is larger, the alphabet can become narrower and more granular.

Granularity follows bandwidth, not the other way around.

## Coarse Alphabets And Fine Alphabets

A coarse alphabet is not a bad alphabet. It is an alphabet matched to a narrow channel.

Examples:
- `2` buckets may only support broad binary distinctions
- `4` to `8` buckets may support large semantic regions
- `16`, `32`, or more buckets may support finer partitioning for complex domains

A low-resolution signal system may only support a few broad semantic continents. A higher-resolution software or domain reasoning workflow may support many smaller semantic regions.

Both are valid. The difference is not quality in the abstract. The difference is available bandwidth.

## Why Over-Fragmentation Is A Problem

An alphabet that is too fine for its channel becomes fragile.

If the system cannot reliably distinguish the number of states implied by the chosen bucket count, then the extra granularity is mostly illusion. It creates false precision without dependable signal support.

That can make downstream interpretation worse rather than better.

A smaller, broader alphabet may be more useful than a larger, unstable one.

## Graceful Degradation

Semantic Signal Alphabet should degrade gracefully when bandwidth is poor.

When a channel is noisy, low-resolution, or ambiguous, the system should be willing to operate with fewer buckets and broader semantic coverage.

This matters because usefulness does not require perfect precision.

A coarse alphabet may still narrow a large space into a smaller candidate region. That can be enough to support ranking, clarification, iterative interaction, or user-guided narrowing.

In some applications, broad buckets are not a failure mode. They are the correct mode.

## Example: Low-Resolution Interpretation

In a low-resolution setting such as an early brainwave or constrained signal interface, the system may only support a very small number of distinguishable patterns.

In that case, the alphabet may contain only a few broad buckets, each holding many possible words or meanings.

If the application can only distinguish six stable signal patterns, then the alphabet should be built around six active buckets. That six-bucket limit is defined by the application constraint. The model's task is to make the best semantic use of those six buckets, not to invent a different bucket count.

That still has value.

Hits across a small number of buckets may narrow the candidate space enough for the interpreter to ask better follow-up questions, rank possible meanings, or refine guesses over time using user-specific interaction history.

The bucket map remains useful even when it is coarse.

## Example: Higher-Resolution Domains

Other domains can support more semantic detail.

A codebase, error taxonomy, project map, or technical domain vocabulary may be partitioned into many more buckets with fewer items in each. That can make routing and interpretation more precise.

In those cases, the application context may justify a much larger bucket count. A coding workflow, physics domain map, or personal project ecosystem may have enough usable structure to support more buckets than a low-resolution signal channel.

The same system principle still applies:
the bucket count should match the usable bandwidth of the problem.

The only difference is that some domains or workflows support more resolution than others.

## Choosing A Bucket Count

A bucket count should be chosen based on practical signal or task constraints, not aesthetic preference.

Useful considerations include:
- how many distinct states can actually be detected or reused
- how noisy or stable the channel is
- how broad or narrow the domain is
- whether the alphabet is meant for first-pass narrowing or finer-grained interpretation
- whether downstream systems can ask clarifying questions or adapt over time

The correct bucket count is the one that creates the most useful semantic compression without pretending to have more precision than the system can sustain.

## Design Rule

Do not optimize for maximum fragmentation.

Optimize for the best semantic coverage that the real bandwidth can support.

That is what it means to say:

`bucket count = bandwidth`

Or more operationally:

- the application sets the bucket number
- the model fills that number with its own semantic sorting logic
