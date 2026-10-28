#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate per-pet, per-platform FILES-<pet>.md from the plugin manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PET = "angelina"
PLATFORMS = ("windows", "harmonyos", "android")
PLATFORM_LABEL = {
    "windows": "Windows",
    "harmonyos": "HarmonyOS",
    "android": "Android",
}

SPINE_MODEL = {
    "build": "基建小人",
    "back": "战斗背面",
    "front": "战斗正面",
}

VOICE_NAMES = {
    "anniv": "周年庆典",
    "assistant": "任命助理",
    "birthday": "生日",
    "deploy1": "部署1",
    "deploy2": "部署2",
    "fight1": "作战中1",
    "fight2": "作战中2",
    "fight3": "作战中3",
    "fight4": "作战中4",
    "greeting": "问候",
    "idle": "闲置",
    "newyear": "新年祝福",
    "poke": "戳一下",
    "promo1": "晋升后交谈1",
    "promo2": "晋升后交谈2",
    "report": "干员报到",
    "select1": "选中干员1",
    "select2": "选中干员2",
    "talk1": "交谈1",
    "talk2": "交谈2",
    "talk3": "交谈3",
    "trust1": "信赖提升后交谈1",
    "trust2": "信赖提升后交谈2",
    "trust3": "信赖提升后交谈3",
}


def human_size(size: int) -> str:
    if size >= 1048576:
        return f"{size / 1048576:.2f} MiB"
    if size >= 1024:
        return f"{size / 1024:.1f} KiB"
    return f"{size} B"


MODEL_NAMES = {
    "angel": "能天使",
    "angel2": "新约能天使",
}


def describe(path: str) -> str:
    p = path.replace("\\", "/")
    name = Path(p).name
    stem = Path(p).stem

    if name == "avatar.png" and "/spine/" not in p:
        return "应用内头像"

    if p.startswith("public/models/"):
        parts = p.split("/")
        model = parts[2] if len(parts) > 2 else ""
        label = MODEL_NAMES.get(model, model or "Spine 模型")
        if "_white" in name:
            label += "（白调光翼）"
        if name.endswith(".skel"):
            return f"{label}：二进制骨架与动画数据"
        if name.endswith(".atlas"):
            return f"{label}：贴图图集描述"
        if name.endswith(".png"):
            return f"{label}：贴图"

    if "/spine/" in p or p.startswith("spine/"):
        parts = p.split("/")
        model = ""
        if "spine" in parts:
            idx = parts.index("spine")
            if idx + 1 < len(parts):
                model = parts[idx + 1]
        label = SPINE_MODEL.get(model, model or "Spine 模型")
        if name.endswith(".skel"):
            return f"{label}：二进制骨架与动画数据"
        if name.endswith(".atlas"):
            return f"{label}：贴图图集描述"
        if name.endswith(".png"):
            return f"{label}：贴图"

    if "/voice_cn/" in p or (p.startswith("voice/") and not p.startswith("voice_jp/")):
        return f"中文语音：{VOICE_NAMES.get(stem, stem)}"
    if "/voice_jp/" in p or p.startswith("voice_jp/"):
        return f"日文语音：{VOICE_NAMES.get(stem, stem)}"
    if "技能图标" in p:
        return f"技能图标：{stem}"

    return "素材文件"


def render(platform: str, manifest: dict) -> str:
    if manifest.get("extract_root") == "app":
        extract_label = "应用目录（Windows 程序所在目录）"
    elif manifest.get("extract_root") == "project":
        extract_label = "项目根目录（解压后素材落在 `public/models/`）"
    else:
        extract_label = f"`filesDir/plugins/{manifest['pet']}/{manifest['asset_version']}/`"
    lines = [
        f"# {PLATFORM_LABEL[platform]} 文件清单（{manifest['pet']}）",
        "",
        f"> 由 `tools/build_file_docs.py` 自动生成；逐文件 SHA-256 见同目录的 `{manifest['pet']}.json`。",
        "",
        f"- 素材包：`{manifest['package']}`",
        f"- 解压根：{extract_label}",
        f"- 文件数：{manifest['file_count']}",
        f"- 整包 SHA-256：`{manifest['sha256']}`",
        "",
        "| 文件 | 大小 | 说明 |",
        "|---|---:|---|",
    ]
    for item in manifest["files"]:
        lines.append(
            f"| `{item['path']}` | {human_size(item['size'])} | {describe(item['path'])} |"
        )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pet", default=DEFAULT_PET)
    args = parser.parse_args()

    for platform in PLATFORMS:
        manifest_path = REPO_ROOT / platform / f"{args.pet}.json"
        if not manifest_path.is_file():
            print(f"skip: {manifest_path}")
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        output = REPO_ROOT / platform / f"FILES-{args.pet}.md"
        output.write_text(render(platform, manifest), encoding="utf-8")
        print(f"wrote {output} ({manifest['file_count']} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
