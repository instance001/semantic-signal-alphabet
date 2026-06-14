# Glossary (Repo Excerpt)

For the full glossary, see: https://github.com/instance001/Whatisthisgithub/blob/main/GLOSSARY.md

This file contains only the glossary entries for this repository. Mapping tag legends and global notes live in the full glossary.

## semantic-signal-alphabet
| Term | Alternate term(s) | Alt map | External map | Relation to existing terminology | What it is | What it is not | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Semantic Signal Alphabet | SSA | = | ~ | Model-native semantic compression framework | Standardized domain-agnostic framework for generating low-bandwidth semantic alphabets where the bucket count is fixed by the application and the target model supplies the compression logic | Not a literal character encoding; not one universal taxonomy for every model or domain | semantic-signal-alphabet/README.md |
| Bucket count = available bandwidth | bucket budget | = | ~ | Bandwidth-allocation principle | Core principle that the application sets the number of buckets the channel can support and the model sorts the source material within that limit | Not maximum granularity by default; not a model-chosen bucket count | semantic-signal-alphabet/README.md |
| Model-native sorting | native sorting | ~ | ~ | Model-specific category-generation stance | Approach where the model builds the bucket map instead of being forced into a human-authored taxonomy first | Not objective proof that one alphabet is universally correct; not human-first classification | semantic-signal-alphabet/README.md |
| Bucket map artifact | bucket map | = | ~ | Frozen semantic map artifact | Versioned saved artifact recording how a specific model partitioned a specific source set under a specific bucket constraint | Not a mutable live memory store; not adapter runtime logic itself | semantic-signal-alphabet/README.md |
| `UNASSIGNED` | unassigned bucket | = | ~ | Honest overflow bucket | Explicit bucket for items that do not fit cleanly into the current bucket structure, preserving uncertainty instead of forcing weak matches | Not a failure state; not a discard pile by default | semantic-signal-alphabet/README.md |
| Adapters are downstream of the core | adapters | ~ | ~ | Core-vs-adapter boundary | Rule that the repository owns generation logic and artifact structure, while application-specific interpreters or routing systems consume the resulting alphabets downstream | Not the definition of the core framework; not a promise of one specific application | semantic-signal-alphabet/README.md |
