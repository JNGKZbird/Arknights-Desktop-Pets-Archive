# Windows 插件定义

`angelina.json` 是予愿安洁莉娜在 Windows 端的插件定义（manifest）。

## 素材包

- 文件：`windows.zip`
- 大小：37,076,957 字节（约 35.4 MiB）
- SHA-256：`71455fe4165eb6d099b4ce4d9cdf399fd438076a9e487739171ee80919c3f60f`
- 下载：Release `angelina-assets-v1`  
  `https://github.com/JNGKZbird/Arknights-Desktop-Pets-Archive/releases/download/angelina-assets-v1/windows.zip`

## zip 内容

解压到 Windows 应用目录后包含：

- `pets/予愿安洁莉娜/spine/`
- `pets/予愿安洁莉娜/voice_cn/`
- `pets/予愿安洁莉娜/voice_jp/`
- `pets/技能图标/`
- `assets/avatar.png`

`manifest.json` 与 `skills/` 仍在 Windows 代码仓库中，不在这个 zip 内。

每个文件的路径、大小和用途见 [FILES.md](FILES.md)。

## 校验与安装

App 从 Release 下载 zip，按 `angelina.json` 校验整包 SHA-256、文件清单和逐文件哈希，通过后解压到本地插件目录。仓库不重复提交 zip，只保留插件定义与说明。
