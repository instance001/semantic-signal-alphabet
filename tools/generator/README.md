# Generator Tool

This folder contains the first core implementation target for Semantic Signal Alphabet.

The generator tool is responsible for creating frozen bucket map artifacts from:
- a source manifest or source item list
- an application-defined bucket count
- a target model
- a prompt version

This tool belongs to the core framework. It is not tied to any one adapter domain.

It should also be understood as a configurable generator. The point is not to hardcode one vocabulary, one bucket count, or one use case. The point is to let users supply the values that match their own application constraints.

## Purpose

The generator tool turns the repository's documentation and schema design into a repeatable artifact-generation workflow.

Its job is to:
- load source data
- accept a fixed bucket count
- use the chosen model to produce a model-native semantic partition
- preserve `UNASSIGNED` items
- validate the result
- save a frozen bucket map artifact

## Core Rule

The generator follows the central rule of the framework:

- the application defines the bucket number
- the model defines the sorting within that number

The tool does not decide how many buckets should exist. It enforces the bucket count given by the application or adapter context.

Users are expected to edit the inputs for their own setups:
- source vocabulary
- bucket count
- model
- prompt version
- domain constraints

## Model-Specific Generation

Generated alphabets are model-specific.

The model that will later interpret or work with a bucket map should be the model used to generate that bucket map in the first place.

If a different model is introduced later, the system should generate a new bucket map with that model before any old user logs are used for runtime adaptation.

## First Version Scope

The first implementation should stay deliberately small.

It only needs to:
- read a source manifest
- accept `bucket_count`
- accept `model`
- accept `prompt_version`
- call the target model
- normalize the response
- validate the output against the bucket map schema
- write a new artifact to disk

The first version does not need:
- runtime interpretation
- multi-model comparison
- adaptive user-history learning
- consensus generation
- a GUI

## Suggested Contents

This folder is expected to hold:
- the first generator script
- any small helper modules needed for normalization or validation
- usage notes specific to the generator tool

The design target for the first implementation is described in [09_generator_tool_spec.md](../../docs/09_generator_tool_spec.md).

## Current Script

The first generator entry point is:

`generate_bucket_map.py`

It supports:
- source manifest JSON input
- direct JSON list input
- plain-text source lists with one item per line
- strict bucket-count enforcement
- schema validation before writing
- offline normalization testing with a saved model response file

## Setup

Install the generator dependency before running the script from a fresh checkout:

```text
python -m pip install -r tools/generator/requirements.txt
```

## Example Usage

Using a source manifest and a live model call:

```text
python tools/generator/generate_bucket_map.py ^
  --source path/to/source_manifest.json ^
  --bucket-count 8 ^
  --model YOUR_MODEL ^
  --prompt-version v1
```

Using a plain-text source list:

```text
python tools/generator/generate_bucket_map.py ^
  --source path/to/english_words.txt ^
  --source-id english-common ^
  --source-name "English Common Word List" ^
  --source-kind word_list ^
  --bucket-count 8 ^
  --model YOUR_MODEL ^
  --prompt-version v1
```

Using a saved model response file for offline testing:

```text
python tools/generator/generate_bucket_map.py ^
  --source path/to/source_manifest.json ^
  --bucket-count 8 ^
  --model test-model ^
  --prompt-version v1 ^
  --response-file path/to/mock_response.json
```

## API Configuration

By default, the script expects an API key in:

`OPENAI_API_KEY`

It also supports:

- `OPENAI_BASE_URL` for an OpenAI-compatible base URL
- `--api-key-env` to point at a different environment variable
- `--api-base-url` to override the base URL directly

## Important Behavior

- The script treats bucket count as application-owned input.
- The script treats generated alphabets as model-specific artifacts.
- The script refuses to overwrite an existing output artifact.
- If a model returns the wrong number of buckets, generation fails rather than silently repairing the result.
- The script is meant to be reused with edited inputs for different domains, vocabularies, bucket counts, and hardware realities.
