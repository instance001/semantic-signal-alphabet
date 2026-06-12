# Adapters Are Not The Core

Semantic Signal Alphabet is a core framework for generating and storing semantic alphabets.

It is not, by itself, a brain-computer interface, a gesture system, a coding assistant, a file router, or a smart-home controller.

Those may become downstream applications. They are not the core definition of the project.

## What The Core Repo Owns

The core repository owns the shared system that downstream tools build on top of.

That includes:
- the conceptual model
- the bucket-generation logic
- the artifact structure
- the schema definitions
- the versioning rules
- the documentation for how alphabets should be created and reused

In other words, the core repo defines how semantic alphabets are made, described, and preserved.

The core repo does not need to solve every application domain in order to be useful.

## What Adapters Own

Adapters are downstream systems that consume a generated alphabet and use it in a specific context.

An adapter might:
- map a signal pattern to likely bucket activations
- route compiler errors into repair workflows
- compress project state into reusable semantic handles
- sort files or artifacts through a constrained bucket space
- help a user navigate a narrow communication channel

One of the adapter's most important jobs is deciding the usable bucket count for its own context. That is how the application tells the core alphabet system what bandwidth is actually available.

The adapter is responsible for the application-specific logic around the alphabet.

That may include:
- input capture
- runtime interpretation
- ranking
- clarification loops
- user interaction
- domain-specific heuristics
- hardware integration

Those concerns belong to the adapter, not the alphabet core.

## Why This Separation Matters

This separation protects the project from becoming vague or overextended.

If the repo tries to define the semantic alphabet framework and every possible application at the same time, the core idea becomes harder to understand and harder to stabilize.

Keeping adapters downstream gives the project several advantages:
- the core artifact model stays reusable
- different applications can share the same generation principles
- hardware-specific or domain-specific complexity does not distort the core framework
- speculative applications do not redefine the project itself

This makes the repository more durable and easier to reason about.

## Example: Brainwave Interpretation

Brainwave or BCI-style communication is one possible adapter category.

In that setting, the alphabet may be very coarse because the signal layer may only support a small number of distinguishable states. A runtime system might observe likely bucket activations, narrow candidate meanings, ask clarifying questions, and improve ranking over time through user interaction.

If that adapter can only support six reliable signal distinctions, then it should request a six-bucket alphabet. The core model then decides how to sort the source material within those six active buckets.

That is a valid and interesting application.

It is still an adapter.

The core repo should not be defined as a brainwave-decoding product. It should be defined as the semantic alphabet framework that a brainwave interpreter might use.

## Example: Code And Project Reasoning

A coding or project adapter might use a generated alphabet to:
- group compiler errors
- route bug types
- compress repository context
- narrow likely repair categories
- structure project-state interpretation

Because these adapters may operate in richer environments, they may choose larger bucket counts than a low-resolution signal interface would. The same rule still applies: the adapter defines the bucket number, and the model defines the sorting.

This is a very different application surface from BCI, but the same core alphabet principles still apply.

That is the value of keeping the core system separate from the application layer.

## Future Adapter Folders

Over time, the repository may include subfolders, tools, or experiments for specific adapters.

Examples might include:
- a brainwave translator prototype
- a code-routing prototype
- a domain vocabulary compressor
- a narrow-topic communication adapter

Those should be introduced only after the core repo is clearly documented.

The shared alphabet model should come first.
The application layers should come later.

## Design Rule

Treat alphabets as the foundation and adapters as consumers.

Do not let any one downstream use case redefine the core project.

The repo should remain centered on the standardized generation and storage of semantic alphabets that can later be applied across many domains.
