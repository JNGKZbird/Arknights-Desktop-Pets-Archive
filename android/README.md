# Android 插件定义

`angelina.json` 是予愿安洁莉娜在 Android 端的插件定义（manifest）。

## 素材包

- 文件：`android.zip`
- 大小：37,184,492 字节（约 35.5 MiB）
- SHA-256：`3955b883a02a1c796f230c39597444dd5237daf095bbe54f63bafbcb1f34dbc8`
- 下载：Release `angelina-assets-v1`  
  `https://github.com/JNGKZbird/Arknights-Desktop-Pets-Archive/releases/download/angelina-assets-v1/android.zip`

## zip 内容

解压到 `filesDir/plugins/angelina/1.0.0/` 后包含：

- `spine/`
- `voice/`
- `voice_jp/`

Skill 文本仍在 Android 代码仓库的 assets 中，不在这个 zip 内。

每个文件的路径、大小和用途见 [FILES-angelina.md](FILES-angelina.md)。

## 校验与安装

App 从 Release 下载 zip，按 `angelina.json` 校验整包 SHA-256、文件清单和逐文件哈希，通过后解压到本地插件目录。仓库不重复提交 zip，只保留插件定义与说明。
