#!/usr/bin/env python3
"""Generate Semantic Signal Alphabet bucket map artifacts."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request
from typing import Any

import jsonschema


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
SCHEMA_DIR = REPO_ROOT / "schemas"
SOURCE_SCHEMA_PATH = SCHEMA_DIR / "source_manifest.schema.json"
BUCKET_SCHEMA_PATH = SCHEMA_DIR / "bucket_map.schema.json"
SCHEMA_VERSION = "0.1.0"
DEFAULT_API_BASE_URL = "https://api.openai.com/v1"
DEFAULT_SYSTEM_PROMPT = (
    "You are generating a Semantic Signal Alphabet bucket map. "
    "The application has already fixed the bucket count. "
    "Your job is to sort the source items into exactly that many active buckets "
    "with broad, useful semantic coverage. "
    "Do not change the bucket count. "
    "Items that do not fit cleanly must go into UNASSIGNED."
)


class GenerationError(Exception):
    """Raised when generation cannot continue safely."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a Semantic Signal Alphabet bucket map from a source manifest "
            "or source item list."
        )
    )
    parser.add_argument(
        "--source",
        required=True,
        help=(
            "Path to a source manifest JSON file, a JSON list of source items, "
            "or a plain-text file containing one item per line."
        ),
    )
    parser.add_argument(
        "--bucket-count",
        required=True,
        type=int,
        help="Application-defined active bucket count.",
    )
    parser.add_argument(
        "--model",
        required=True,
        help="Target model identifier used to generate the bucket map.",
    )
    parser.add_argument(
        "--prompt-version",
        required=True,
        help="Prompt version identifier to record in the output artifact.",
    )
    parser.add_argument(
        "--domain-constraint",
        action="append",
        default=[],
        help="Optional domain or theme constraint. Repeat to supply more than one.",
    )
    parser.add_argument(
        "--notes",
        help="Optional artifact notes to save with the generated bucket map.",
    )
    parser.add_argument(
        "--artifact-id",
        help="Optional stable artifact identifier.",
    )
    parser.add_argument(
        "--output",
        help="Optional explicit output path for the generated artifact.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.2,
        help="Sampling temperature for the model call. Defaults to 0.2.",
    )
    parser.add_argument(
        "--api-base-url",
        default=os.environ.get("OPENAI_BASE_URL", DEFAULT_API_BASE_URL),
        help=(
            "Base URL for an OpenAI-compatible API. Defaults to OPENAI_BASE_URL "
            f"or {DEFAULT_API_BASE_URL}."
        ),
    )
    parser.add_argument(
        "--api-key-env",
        default="OPENAI_API_KEY",
        help="Environment variable containing the API key. Defaults to OPENAI_API_KEY.",
    )
    parser.add_argument(
        "--response-file",
        help=(
            "Optional path to a JSON file containing a saved model response object. "
            "When provided, the script skips the live API call and normalizes this response."
        ),
    )
    parser.add_argument(
        "--source-id",
        help="Required when --source is not a source manifest.",
    )
    parser.add_argument(
        "--source-name",
        help="Required when --source is not a source manifest.",
    )
    parser.add_argument(
        "--source-kind",
        help="Required when --source is not a source manifest.",
    )
    return parser.parse_args()


def load_json(path: pathlib.Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def load_schema(path: pathlib.Path) -> dict[str, Any]:
    data = load_json(path)
    if not isinstance(data, dict):
        raise GenerationError(f"Schema file is not a JSON object: {path}")
    return data


def validate_with_schema(instance: Any, schema_path: pathlib.Path) -> None:
    schema = load_schema(schema_path)
    jsonschema.validate(instance=instance, schema=schema)


def normalize_item(value: Any) -> dict[str, str]:
    if isinstance(value, str):
        cleaned = value.strip()
        if not cleaned:
            raise GenerationError("Encountered an empty string item.")
        return {"value": cleaned}
    if isinstance(value, dict):
        raw_value = value.get("value")
        if not isinstance(raw_value, str) or not raw_value.strip():
            raise GenerationError("Item objects must contain a non-empty string 'value'.")
        normalized = {"value": raw_value.strip()}
        notes = value.get("notes")
        if notes is not None:
            if not isinstance(notes, str):
                raise GenerationError("Item 'notes' must be a string when present.")
            normalized["notes"] = notes
        return normalized
    raise GenerationError(f"Unsupported item shape: {value!r}")


def ensure_non_manifest_metadata(args: argparse.Namespace) -> None:
    missing = []
    if not args.source_id:
        missing.append("--source-id")
    if not args.source_name:
        missing.append("--source-name")
    if not args.source_kind:
        missing.append("--source-kind")
    if missing:
        joined = ", ".join(missing)
        raise GenerationError(
            f"Non-manifest sources require explicit metadata. Missing: {joined}"
        )


def normalize_source_manifest(args: argparse.Namespace) -> dict[str, Any]:
    source_path = pathlib.Path(args.source).resolve()
    if not source_path.exists():
        raise GenerationError(f"Source file does not exist: {source_path}")

    suffix = source_path.suffix.lower()
    if suffix == ".json":
        raw_json = load_json(source_path)
        if isinstance(raw_json, dict) and raw_json.get("manifest_type") == "source_manifest":
            validate_with_schema(raw_json, SOURCE_SCHEMA_PATH)
            return raw_json
        if isinstance(raw_json, list):
            ensure_non_manifest_metadata(args)
            items = [normalize_item(item) for item in raw_json]
            manifest = {
                "schema_version": SCHEMA_VERSION,
                "manifest_type": "source_manifest",
                "source_id": args.source_id,
                "source_name": args.source_name,
                "source_kind": args.source_kind,
                "source_uri": str(source_path),
                "domain_constraints": args.domain_constraint or None,
                "items": items,
            }
            if manifest["domain_constraints"] is None:
                manifest.pop("domain_constraints")
            validate_with_schema(manifest, SOURCE_SCHEMA_PATH)
            return manifest
        raise GenerationError(
            "JSON source files must be either a source manifest object or a JSON list of items."
        )

    ensure_non_manifest_metadata(args)
    with source_path.open("r", encoding="utf-8") as handle:
        lines = [line.strip() for line in handle.readlines()]
    items = [normalize_item(line) for line in lines if line]
    if not items:
        raise GenerationError(f"Source item list is empty: {source_path}")
    manifest = {
        "schema_version": SCHEMA_VERSION,
        "manifest_type": "source_manifest",
        "source_id": args.source_id,
        "source_name": args.source_name,
        "source_kind": args.source_kind,
        "source_uri": str(source_path),
        "domain_constraints": args.domain_constraint or None,
        "items": items,
    }
    if manifest["domain_constraints"] is None:
        manifest.pop("domain_constraints")
    validate_with_schema(manifest, SOURCE_SCHEMA_PATH)
    return manifest


def build_user_prompt(
    source_manifest: dict[str, Any],
    bucket_count: int,
    prompt_version: str,
    domain_constraints: list[str],
) -> str:
    source_items = [item["value"] for item in source_manifest["items"]]
    constraints_text = (
        "\n".join(f"- {constraint}" for constraint in domain_constraints)
        if domain_constraints
        else "- None"
    )
    payload = {
        "prompt_version": prompt_version,
        "source_manifest": {
            "source_id": source_manifest["source_id"],
            "source_name": source_manifest["source_name"],
            "source_kind": source_manifest["source_kind"],
            "item_count": len(source_items),
        },
        "bucket_count": bucket_count,
        "domain_constraints": domain_constraints,
        "items": source_items,
    }
    return (
        "Generate a Semantic Signal Alphabet bucket map.\n\n"
        "Rules:\n"
        f"- Return exactly {bucket_count} active buckets.\n"
        "- The bucket count is fixed by the application. Do not change it.\n"
        "- Full coverage is not expected.\n"
        "- Prioritize broad, useful semantic coverage.\n"
        "- Place items that do not fit cleanly into UNASSIGNED.\n"
        "- Return valid JSON only with this shape:\n"
        '{\n'
        '  "buckets": [\n'
        '    {\n'
        '      "bucket_id": "B1",\n'
        '      "label": "string",\n'
        '      "summary": "string",\n'
        '      "anchor_items": ["string"],\n'
        '      "assigned_items": ["string"]\n'
        '    }\n'
        "  ],\n"
        '  "unassigned_items": ["string"]\n'
        "}\n\n"
        f"Domain constraints:\n{constraints_text}\n\n"
        "Source payload:\n"
        f"{json.dumps(payload, ensure_ascii=True, indent=2)}\n"
    )


def extract_content_from_response(payload: dict[str, Any]) -> str:
    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices:
        raise GenerationError("Model response did not include any choices.")
    first = choices[0]
    if not isinstance(first, dict):
        raise GenerationError("Malformed model response choice.")
    message = first.get("message")
    if not isinstance(message, dict):
        raise GenerationError("Model response choice did not include a message.")
    content = message.get("content")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for part in content:
            if isinstance(part, dict):
                text = part.get("text")
                if isinstance(text, str):
                    parts.append(text)
        if parts:
            return "\n".join(parts)
    raise GenerationError("Unable to extract text content from model response.")


def strip_code_fences(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    return stripped.strip()


def load_model_response(args: argparse.Namespace, prompt: str) -> dict[str, Any]:
    if args.response_file:
        response_path = pathlib.Path(args.response_file).resolve()
        if not response_path.exists():
            raise GenerationError(f"Response file does not exist: {response_path}")
        payload = load_json(response_path)
        if not isinstance(payload, dict):
            raise GenerationError("Response file must contain a JSON object.")
        return payload

    api_key = os.environ.get(args.api_key_env)
    if not api_key:
        raise GenerationError(
            f"Missing API key in environment variable {args.api_key_env}. "
            "Set it or use --response-file for offline normalization testing."
        )

    url = args.api_base_url.rstrip("/") + "/chat/completions"
    body = {
        "model": args.model,
        "temperature": args.temperature,
        "messages": [
            {"role": "system", "content": DEFAULT_SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise GenerationError(
            f"Model API request failed with HTTP {exc.code}: {detail}"
        ) from exc
    except urllib.error.URLError as exc:
        raise GenerationError(f"Model API request failed: {exc}") from exc

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise GenerationError(f"Model API response was not valid JSON: {exc}") from exc

    if not isinstance(payload, dict):
        raise GenerationError("Model API response root must be a JSON object.")
    return payload


def parse_model_output(payload: dict[str, Any]) -> dict[str, Any]:
    content = extract_content_from_response(payload)
    cleaned = strip_code_fences(content)
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise GenerationError(
            "Model content was not valid JSON after extraction."
        ) from exc
    if not isinstance(parsed, dict):
        raise GenerationError("Model output JSON must be an object.")
    return parsed


def normalize_item_list(raw_items: Any, field_name: str) -> list[dict[str, str]]:
    if raw_items is None:
        return []
    if not isinstance(raw_items, list):
        raise GenerationError(f"'{field_name}' must be a list.")
    return [normalize_item(item) for item in raw_items]


def normalize_buckets(model_output: dict[str, Any], bucket_count: int) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    raw_buckets = model_output.get("buckets")
    if not isinstance(raw_buckets, list):
        raise GenerationError("Model output must include a 'buckets' list.")
    if len(raw_buckets) != bucket_count:
        raise GenerationError(
            f"Model returned {len(raw_buckets)} buckets, expected exactly {bucket_count}."
        )

    normalized_buckets: list[dict[str, Any]] = []
    for index, raw_bucket in enumerate(raw_buckets, start=1):
        if not isinstance(raw_bucket, dict):
            raise GenerationError(f"Bucket {index} must be a JSON object.")
        label = raw_bucket.get("label")
        summary = raw_bucket.get("summary")
        if not isinstance(label, str) or not label.strip():
            raise GenerationError(f"Bucket {index} is missing a non-empty 'label'.")
        if not isinstance(summary, str) or not summary.strip():
            raise GenerationError(f"Bucket {index} is missing a non-empty 'summary'.")
        bucket_id = raw_bucket.get("bucket_id")
        if not isinstance(bucket_id, str) or not bucket_id.strip():
            bucket_id = f"B{index}"
        normalized_buckets.append(
            {
                "bucket_id": bucket_id.strip(),
                "label": label.strip(),
                "summary": summary.strip(),
                "anchor_items": normalize_item_list(
                    raw_bucket.get("anchor_items"), f"buckets[{index}].anchor_items"
                ),
                "assigned_items": normalize_item_list(
                    raw_bucket.get("assigned_items"), f"buckets[{index}].assigned_items"
                ),
            }
        )

    unassigned_raw = model_output.get("unassigned_items", model_output.get("UNASSIGNED"))
    unassigned_items = normalize_item_list(unassigned_raw, "unassigned_items")
    return normalized_buckets, unassigned_items


def sanitize_path_part(value: str) -> str:
    lowered = value.strip().lower()
    safe = re.sub(r"[^a-z0-9._-]+", "-", lowered)
    safe = safe.strip("-")
    return safe or "artifact"


def default_output_path(source_manifest: dict[str, Any], model: str, bucket_count: int) -> pathlib.Path:
    timestamp = dt.datetime.now(dt.UTC).strftime("%Y%m%dT%H%M%SZ")
    return (
        REPO_ROOT
        / "artifacts"
        / sanitize_path_part(source_manifest["source_id"])
        / sanitize_path_part(model)
        / str(bucket_count)
        / f"{timestamp}.json"
    )


def build_artifact(
    args: argparse.Namespace,
    source_manifest: dict[str, Any],
    buckets: list[dict[str, Any]],
    unassigned_items: list[dict[str, str]],
) -> dict[str, Any]:
    created_at = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    artifact: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "artifact_type": "bucket_map",
        "model": args.model,
        "prompt_version": args.prompt_version,
        "bucket_count": args.bucket_count,
        "source_manifest": {
            "source_id": source_manifest["source_id"],
            "source_name": source_manifest["source_name"],
            "source_kind": source_manifest["source_kind"],
        },
        "created_at": created_at,
        "buckets": buckets,
        "unassigned_items": unassigned_items,
    }
    if "source_version" in source_manifest:
        artifact["source_manifest"]["source_version"] = source_manifest["source_version"]
    if "source_uri" in source_manifest:
        artifact["source_manifest"]["source_uri"] = source_manifest["source_uri"]
    if args.artifact_id:
        artifact["artifact_id"] = args.artifact_id
    if args.notes:
        artifact["notes"] = args.notes
    return artifact


def write_artifact(artifact: dict[str, Any], output_path: pathlib.Path) -> None:
    if output_path.exists():
        raise GenerationError(f"Refusing to overwrite existing artifact: {output_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(artifact, handle, ensure_ascii=True, indent=2)
        handle.write("\n")


def main() -> int:
    args = parse_args()
    if args.bucket_count < 1:
        raise GenerationError("--bucket-count must be a positive integer.")

    source_manifest = normalize_source_manifest(args)
    prompt = build_user_prompt(
        source_manifest=source_manifest,
        bucket_count=args.bucket_count,
        prompt_version=args.prompt_version,
        domain_constraints=args.domain_constraint,
    )
    raw_response = load_model_response(args, prompt)
    model_output = parse_model_output(raw_response)
    buckets, unassigned_items = normalize_buckets(model_output, args.bucket_count)
    artifact = build_artifact(args, source_manifest, buckets, unassigned_items)
    validate_with_schema(artifact, BUCKET_SCHEMA_PATH)

    output_path = (
        pathlib.Path(args.output).resolve()
        if args.output
        else default_output_path(source_manifest, args.model, args.bucket_count)
    )
    write_artifact(artifact, output_path)

    print(f"Generated bucket map: {output_path}")
    print(f"Source items: {len(source_manifest['items'])}")
    print(f"Buckets: {len(buckets)}")
    print(f"Unassigned items: {len(unassigned_items)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except GenerationError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
    except jsonschema.ValidationError as exc:
        print(f"Schema validation failed: {exc.message}", file=sys.stderr)
        raise SystemExit(1)
