# HarmonyOS 插件定义

`angelina.json` 是予愿安洁莉娜在 HarmonyOS 端的插件定义（manifest）。

## 素材包

- 文件：`harmonyos.zip`
- 大小：37,287,701 字节（约 35.6 MiB）
- SHA-256：`b2e9ab1d3e60489969d0eeadcc805e441644178a076c83601d4b5f7b60449623`
- 下载：Release `angelina-assets-v1`  
  `https://github.com/JNGKZbird/Arknights-Desktop-Pets-Archive/releases/download/angelina-assets-v1/harmonyos.zip`

## zip 内容

解压到 `filesDir/plugins/angelina/1.0.0/` 后包含：

- `spine/`
- `voice/`
- `voice_jp/`
- `avatar.png`

Skill 文本仍在 HarmonyOS 代码仓库的 rawfile 中，不在这个 zip 内。

每个文件的路径、大小和用途见 [FILES.md](FILES.md)。

## 校验与安装

App 从 Release 下载 zip，按 `angelina.json` 校验整包 SHA-256、文件清单和逐文件哈希，通过后解压到本地插件目录。仓库不重复提交 zip，只保留插件定义与说明。
