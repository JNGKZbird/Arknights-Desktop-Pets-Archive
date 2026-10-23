#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build per-pet, per-platform asset packages for the desktop pets.

This repository is shared by multiple pets (Angelina first; the troublemaker
pet will be added later). Assets are copyrighted by Hypergryph; this script
only packages files that already exist on the local machine and grants no
license.

The repository name is final: Arknights-Desktop-Pets-Archive. Pass --base-url
only for a temporary mirror or local testing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = REPO_ROOT / "dist"
DEFAULT_MANIFEST_DIR = REPO_ROOT
DEFAULT_VERSION = "1.0.0"
DEFAULT_PET = "angelina"
DEFAULT_REPO_SLUG = "JNGKZbird/Arknights-Desktop-Pets-Archive"
DEFAULT_BASE_URL = f"https://github.com/{DEFAULT_REPO_SLUG}/releases/download"

SKIP_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini"}

PET_SPECS = {
    "angelina": {
        "display_name": "予愿安洁莉娜",
        "roots": {
            "windows": Path(r"D:\Angelina-pet-芋圆-windows版"),
            "harmonyos": Path(r"D:\Arknights-Angelina-pet"),
            "android": Path(r"D:\Angelina-pet-芋圆-安卓版"),
        },
        "platforms": {
            "windows": {
                "extract_root": "app",
                "entries": [
                    ("pets/予愿安洁莉娜/spine", "pets/予愿安洁莉娜/spine"),
                    ("pets/予愿安洁莉娜/voice_cn", "pets/予愿安洁莉娜/voice_cn"),
                    ("pets/予愿安洁莉娜/voice_jp", "pets/予愿安洁莉娜/voice_jp"),
                    ("pets/技能图标", "pets/技能图标"),
                    ("assets/avatar.png", "assets/avatar.png"),
                ],
            },
            "harmonyos": {
                "extract_root": "plugin",
                "entries": [
                    ("entry/src/main/resources/rawfile/spine", "spine"),
                    ("entry/src/main/resources/rawfile/voice", "voice"),
                    ("entry/src/main/resources/rawfile/voice_jp", "voice_jp"),
                    ("entry/src/main/resources/rawfile/avatar.png", "avatar.png"),
                ],
            },
            "android": {
                "extract_root": "plugin",
                "entries": [
                    ("app/src/main/assets/spine", "spine"),
                    ("app/src/main/assets/voice", "voice"),
                    ("app/src/main/assets/voice_jp", "voice_jp"),
                ],
            },
        },
    },
    # Future pets (for example the troublemaker desktop pet) add their own
    # spec here. Keep each pet's source roots and package entries separate.
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect_entries(root: Path, spec: dict) -> list[tuple[Path, str]]:
    result: list[tuple[Path, str]] = []
    seen: set[str] = set()
    for source_rel, dest in spec["entries"]:
        source = root / source_rel
        if not source.exists():
            raise FileNotFoundError(f"missing source: {source}")
        if source.is_file():
            candidates = [(source, dest)]
        else:
            candidates = []
            for path in sorted(source.rglob("*")):
                if not path.is_file() or path.name in SKIP_NAMES:
                    continue
                rel = path.relative_to(source).as_posix()
                candidates.append((path, f"{dest.rstrip('/')}/{rel}"))
        for path, arcname in candidates:
            normalized = arcname.replace("\\", "/").lstrip("/")
            if ".." in normalized.split("/"):
                raise ValueError(f"unsafe archive path: {arcname}")
            if normalized in seen:
                raise ValueError(f"duplicate archive path: {arcname}")
            seen.add(normalized)
            result.append((path, normalized))
    result.sort(key=lambda item: item[1])
    return result


def build_platform(pet: str, platform: str, root: Path, args: argparse.Namespace) -> dict:
    pet_spec = PET_SPECS[pet]
    spec = pet_spec["platforms"][platform]
    entries = collect_entries(root, spec)
    if not entries:
        raise RuntimeError(f"no files collected for {pet}/{platform}")

    tag = args.tag
    if not tag:
        major = str(args.version).split(".")[0]
        tag = f"{pet}-assets-v{major}"

    out_dir = args.out / pet
    out_dir.mkdir(parents=True, exist_ok=True)
    zip_path = out_dir / f"{platform}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path, arcname in entries:
            zf.write(path, arcname=arcname)

    with zipfile.ZipFile(zip_path, "r") as zf:
        bad = zf.testzip()
        if bad:
            raise RuntimeError(f"corrupt zip entry: {bad}")
        actual = set(zf.namelist())
        expected = {arc for _, arc in entries}
        if actual != expected:
            raise RuntimeError("zip entries do not match the collected file list")

    files = [
        {
            "path": arc,
            "size": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path, arc in entries
    ]
    manifest = {
        "schema": 1,
        "pet": pet,
        "pet_name": pet_spec.get("display_name", pet),
        "platform": platform,
        "asset_version": args.version,
        "release_tag": tag,
        "package": zip_path.name,
        "url": f"{args.base_url.rstrip('/')}/{tag}/{zip_path.name}",
        "sha256": sha256_file(zip_path),
        "size": zip_path.stat().st_size,
        "file_count": len(files),
        "uncompressed_size": sum(item["size"] for item in files),
        "extract_root": spec["extract_root"],
        "files": files,
        "notice": (
            "Assets are copyright Hypergryph. No license is granted. "
            "Personal non-commercial use only."
        ),
    }

    manifest_dir = args.manifest_dir / platform
    manifest_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = manifest_dir / f"{pet}.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        f"[{pet}/{platform}] {len(files)} files, "
        f"{manifest['uncompressed_size'] / 1048576:.1f} MB uncompressed -> "
        f"{zip_path} ({manifest['size'] / 1048576:.1f} MB zip)"
    )
    print(f"  tag: {tag}")
    print(f"  sha256: {manifest['sha256']}")
    print(f"  manifest: {manifest_path}")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pet", choices=sorted(PET_SPECS), default=DEFAULT_PET)
    parser.add_argument(
        "--platform",
        choices=["windows", "harmonyos", "android", "all"],
        default="windows",
    )
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument("--tag", default=None)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--manifest-dir", type=Path, default=DEFAULT_MANIFEST_DIR)
    parser.add_argument("--windows-root", type=Path, default=None)
    parser.add_argument("--harmonyos-root", type=Path, default=None)
    parser.add_argument("--android-root", type=Path, default=None)
    args = parser.parse_args()

    pet_spec = PET_SPECS[args.pet]
    overrides = {
        "windows": args.windows_root,
        "harmonyos": args.harmonyos_root,
        "android": args.android_root,
    }
    platforms = list(pet_spec["platforms"])
    if args.platform != "all":
        platforms = [args.platform]

    for platform in platforms:
        root = overrides[platform] or pet_spec["roots"][platform]
        if not root.is_dir():
            print(f"error: source root not found: {root}", file=sys.stderr)
            return 1
        build_platform(args.pet, platform, root, args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
