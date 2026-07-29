# BCI Adapter

This folder is reserved for brain-computer interface and brain-signal-related adapter work built on top of Semantic Signal Alphabet.

BCI is one downstream application of the framework. It is not the definition of the core project.

This adapter should be read as a reference pattern, not as a fixed or canonical BCI configuration.

## Why BCI Fits This Framework

A BCI-style communication system is often heavily bandwidth-constrained.

If an application can only distinguish a small number of reliable signal patterns, then the alphabet it uses must be coarse. Semantic Signal Alphabet is designed for exactly that situation:

- the application defines the bucket number based on signal reality
- the model defines the sorting within that fixed number

If a BCI setup can only support six distinct signal patterns, then the active alphabet should be generated for six buckets. The model's job is to decide how to use those six buckets as effectively as possible, while still preserving `UNASSIGNED` for items that do not fit cleanly.

Another user may have a very different setup:
- a different number of reliable signal distinctions
- a different vocabulary size
- a narrower or broader communication scope
- a different calibration strategy

The adapter pattern stays the same even when those values change.

## Intended Flow

At a high level, a BCI adapter built on this framework would:

1. choose a source vocabulary or domain word set
2. set the bucket count based on actual signal resolution
3. use the target model to generate a bucket map for that exact bucket count
4. freeze the resulting model-specific artifact
5. use runtime signal hits to narrow candidate semantic regions
6. rank or clarify likely meanings over time

The bucket map is the stable semantic reference.
The runtime interpreter built on top of it may still adapt.

## Coarse Buckets Still Help

A six-bucket alphabet will likely contain broad semantic regions rather than highly specific words.

That is still useful.

A BCI runtime system may observe which buckets are most likely active, then search within the words or meanings associated with those buckets to propose likely interpretations. Over time, clarification loops and user interaction history may help narrow those candidates further.

The point is not to claim perfect direct decoding. The point is to narrow a large meaning space under strict signal limits.

For a worked example of this companion-layer pattern, including a citation to a concrete non-invasive brain-to-text system, see `docs/11_companion_layer_for_partial_signal_decoding.md`.

## Model-Specific Rule

BCI adapters should follow the same model-specific rule as the rest of the framework.

- generate the bucket map with the model you intend to use
- do not preload old user logs before bucket generation
- if the model changes, generate a fresh bucket map first
- only then use historical logs to help the runtime layer adapt to the user's established patterns

This preserves the model-native logic of the alphabet while still allowing user-specific refinement afterward.

## Current Status

This folder is currently documentation-first.

Future contents may include:
- a BCI-specific source vocabulary example
- an adapter-specific runtime design note
- prototype tooling for mapping signal patterns to bucket activations
- evaluation notes for low-bandwidth communication workflows

Any implementation here should remain downstream of the core generator and shared artifact model.

## Included Starter Assets

This adapter now includes:
- [sources/google-10000-english.txt](sources/google-10000-english.txt) as a practical common-English starter list
- [sources/bci_english_google_10000.source_manifest.json](sources/bci_english_google_10000.source_manifest.json) as a generator-ready source manifest
- [triangulation_runtime.md](triangulation_runtime.md) as the runtime design note

These are starter examples only. Users should expect to edit the vocabulary, bucket count, and other inputs to match their own hardware capabilities, calibration methods, and intended communication scope.
