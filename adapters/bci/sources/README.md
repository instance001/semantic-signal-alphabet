# BCI Source Vocabularies

This folder holds source vocabularies and source manifests for BCI-oriented Semantic Signal Alphabet experiments.

For early BCI-style work, a practical common-word vocabulary is a better starting point than an exhaustive dictionary. Low-bandwidth triangulation benefits from:
- common words appearing more often in likely communication
- fewer rare or obscure words competing during ranking
- a bounded search space that is still broad enough for useful experiments

## Current Starter Source

`google-10000-english.txt`

This is a 10,000-word common-English list derived from the `first20hours/google-10000-english` project.

It is included as a practical starter source, not as a required default.

Why this is a good first BCI source:
- it is broad enough for general communication experiments
- it is much smaller than a 400k+ dictionary-style list
- it better matches the idea of practical candidate narrowing under coarse signal limits

## Ready-To-Use Manifest

`bci_english_google_10000.source_manifest.json`

This manifest wraps the word list in the source-manifest schema so the generator can consume it directly.

Users should expect to edit or replace this manifest for their own use cases.

## Notes

- This is a starter vocabulary, not a final canonical English source.
- Later BCI experiments may benefit from narrower scoped vocabularies such as emotions, household requests, people, actions, or project-specific terms.
- Scoped vocabularies should usually converge faster than a broad general-English list.
- Other users may prefer much larger or much smaller vocabularies depending on hardware capability, bandwidth, and intended scope.
