# UNASSIGNED And Wildcard Space

Semantic Signal Alphabet does not require full coverage.

If an item does not fit cleanly into the available semantic buckets, it should not be forced into a weak or misleading placement. It should remain `UNASSIGNED`.

This is a core design choice, not an error condition.

## Why Full Coverage Is Not Required

The system is designed for useful compression under constraint.

A fixed bucket limit means some source items may fit well, some may fit loosely, and some may not fit cleanly at all. That is normal.

Forcing every item into one of the active buckets can create false certainty. It makes the alphabet look more complete than it really is, while quietly degrading its meaning.

Semantic Signal Alphabet treats incomplete coverage as acceptable when the alternative is distortion.

## Why Forced Placement Is Harmful

An item that does not belong cleanly in any active bucket still carries information.

If it is forced into a poor match, the system loses that information and replaces it with a misleading signal. Downstream interpreters may then treat the placement as meaningful when it was really a compromise.

That is worse than leaving the item unresolved.

`UNASSIGNED` protects the integrity of the alphabet by preserving uncertainty instead of hiding it.

## UNASSIGNED As Honest Overflow

The most basic role of `UNASSIGNED` is honest overflow.

It holds:
- items that do not fit the current bucket map cleanly
- items that are too ambiguous for confident placement
- items that may require more granularity than the current bucket count allows
- items that fall outside the useful coverage target of the present alphabet

This is not a failure to complete the task.
It is a truthful reflection of the current compression limit.

## UNASSIGNED As Signal

`UNASSIGNED` is not just leftover material. It is also feedback.

A growing or recurring `UNASSIGNED` set may indicate:
- the bucket count is too low for the source domain
- the current partition leaves important regions uncovered
- a narrower source window may be needed
- a different alphabet may be useful for a different context or theme

In that sense, `UNASSIGNED` acts as a pressure gauge for the current alphabet design.

It shows where the present system stops being clean.

## UNASSIGNED As Wildcard Space

In some downstream applications, `UNASSIGNED` may be operationally useful in its own right.

It can function as:
- an ambiguity set
- a fallback class
- an edge-case pool
- a wildcard region for uncertain or weak matches
- a data collection zone for later analysis

This matters because not every runtime system needs a hard assignment at every step.

Some systems benefit from explicitly preserving uncertainty, then using that uncertainty in later ranking, tie-breaking, refinement, or follow-up interaction.

`UNASSIGNED` can therefore be part of the runtime logic rather than just a discard bucket.

## Future Refinement

`UNASSIGNED` can also help shape later versions of the alphabet.

Repeated patterns in `UNASSIGNED` may suggest:
- a bucket that should be split
- a missing semantic region
- a need for a higher bucket count
- a need for a narrower domain-specific alphabet
- a separate adapter behavior for edge cases

This makes `UNASSIGNED` a useful source of future design evidence.

It is not only overflow from the current map.
It is also input into later map improvement.

## Design Rule

Do not force completeness for appearances.

If an item does not fit, leave it `UNASSIGNED`.

Preserved uncertainty is more useful than fabricated certainty.
