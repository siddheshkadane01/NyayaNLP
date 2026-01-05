"""Dataset acquisition (Step 1).

Downloads datasets that are available via Hugging Face Datasets and stores them under `data/raw/`.

By default this script downloads InLegalNER:
  - HF id: opennyaiorg/InLegalNER

It also writes/updates: data/raw/datasets_manifest.json

Usage:
  .venv/bin/python data/download_datasets.py --inlegalner
  .venv/bin/python data/download_datasets.py --all
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from datasets import DatasetDict, load_dataset


RAW_DIR = Path("data") / "raw"
MANIFEST_PATH = RAW_DIR / "datasets_manifest.json"


@dataclass
class DatasetEntry:
    key: str
    status: str  # downloaded | failed
    source: str
    hf_id: str | None
    saved_to: str
    downloaded_at_utc: str
    error: str | None
    details: dict[str, Any]


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def _load_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.exists():
        return {"version": 1, "datasets": []}
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def _write_manifest(manifest: dict[str, Any]) -> None:
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _upsert_entry(manifest: dict[str, Any], entry: DatasetEntry) -> None:
    datasets: list[dict[str, Any]] = manifest.get("datasets", [])
    datasets = [d for d in datasets if d.get("key") != entry.key]
    datasets.append(asdict(entry))
    datasets.sort(key=lambda d: d.get("key", ""))
    manifest["datasets"] = datasets


def download_inlegalner() -> DatasetEntry:
    key = "inlegalner"
    hf_id = "opennyaiorg/InLegalNER"

    dest = RAW_DIR / key
    _ensure_dir(dest)

    print(f"Downloading {key} from Hugging Face: {hf_id}")
    dataset: DatasetDict = load_dataset(hf_id)  # type: ignore[assignment]

    print(f"Saving to disk: {dest}")
    dataset.save_to_disk(str(dest))

    split_sizes = {split: int(ds.num_rows) for split, ds in dataset.items()}
    features = {split: list(map(str, ds.features.keys())) for split, ds in dataset.items()}

    return DatasetEntry(
        key=key,
        status="downloaded",
        source="huggingface_datasets",
        hf_id=hf_id,
        saved_to=str(dest.as_posix()),
        downloaded_at_utc=_utc_now_iso(),
        error=None,
        details={
            "splits": split_sizes,
            "feature_keys": features,
        },
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Step 1: download datasets into data/raw")
    parser.add_argument("--inlegalner", action="store_true", help="Download InLegalNER (recommended)")
    parser.add_argument("--all", action="store_true", help="Download all known HF-hosted datasets")
    args = parser.parse_args()

    _ensure_dir(RAW_DIR)

    to_run: list[str] = []
    if args.all:
        to_run = ["inlegalner"]
    elif args.inlegalner:
        to_run = ["inlegalner"]
    else:
        # Default behavior: download InLegalNER
        to_run = ["inlegalner"]

    manifest = _load_manifest()

    for key in to_run:
        try:
            if key == "inlegalner":
                entry = download_inlegalner()
            else:
                raise ValueError(f"Unknown dataset key: {key}")

            _upsert_entry(manifest, entry)
            _write_manifest(manifest)
            print(f"Done: {key}")
        except Exception as exc:
            error_text = str(exc)
            print(f"Failed: {key}: {error_text}")

            hint_lines = [
                "If this is a permissions issue:",
                "  1) Visit the dataset page on Hugging Face and request/accept access if required.",
                "  2) Run: huggingface-cli login",
                "  3) Re-run this script.",
            ]
            print("\n".join(hint_lines))

            # Record the failure in the manifest as well.
            failed_dest = (RAW_DIR / key).as_posix()
            failed_entry = DatasetEntry(
                key=key,
                status="failed",
                source="huggingface_datasets",
                hf_id="opennyaiorg/InLegalNER" if key == "inlegalner" else None,
                saved_to=failed_dest,
                downloaded_at_utc=_utc_now_iso(),
                error=error_text,
                details={},
            )
            _upsert_entry(manifest, failed_entry)
            _write_manifest(manifest)

    print(f"Manifest written: {MANIFEST_PATH}")


if __name__ == "__main__":
    # Avoid HF parallelism surprises
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
    main()
