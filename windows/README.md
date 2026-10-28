# Windows 插件定义

本目录存放 Windows 端各宠物的插件定义（manifest）与素材包说明。

| pet | 角色 | manifest | 逐文件清单 |
|---|---|---|---|
| `angelina` | 予愿安洁莉娜 | `angelina.json` | [FILES-angelina.md](FILES-angelina.md) |
| `trickster` | 捣蛋鬼（能天使 / 新约能天使） | `trickster.json` | [FILES-trickster.md](FILES-trickster.md) |

## angelina

`angelina.json` 是予愿安洁莉娜在 Windows 端的插件定义。

- 文件：`windows.zip`
- 大小：37,076,957 字节（约 35.4 MiB）
- SHA-256：`71455fe4165eb6d099b4ce4d9cdf399fd438076a9e487739171ee80919c3f60f`
- 下载：Release `angelina-assets-v1`  
  `https://github.com/JNGKZbird/Arknights-Desktop-Pets-Archive/releases/download/angelina-assets-v1/windows.zip`

### zip 内容

解压到 Windows 应用目录后包含：

- `pets/予愿安洁莉娜/spine/`
- `pets/予愿安洁莉娜/voice_cn/`
- `pets/予愿安洁莉娜/voice_jp/`
- `pets/技能图标/`
- `assets/avatar.png`

`manifest.json` 与 `skills/` 仍在 Windows 代码仓库中，不在这个 zip 内。

每个文件的路径、大小和用途见 [FILES-angelina.md](FILES-angelina.md)。

## trickster

`trickster.json` 是捣蛋鬼在 Windows 端的插件定义。角色为能天使与新约能天使。

- 文件：`windows.zip`
- 大小：975,229 字节（约 0.9 MiB）
- SHA-256：`08cedc78254fc3ab4d370d15e7cdf65f98fc415b751a98e33bc9702c267ab87d`
- 下载：Release `trickster-assets-v1`  
  `https://github.com/JNGKZbird/Arknights-Desktop-Pets-Archive/releases/download/trickster-assets-v1/windows.zip`

### zip 内容

解压到项目根目录后包含：

- `public/models/angel/` — 能天使：基建 Q 版默认皮与白调光翼变体
- `public/models/angel2/` — 新约能天使：基建 Q 版默认皮

当前只含能天使 / 新约能天使的基建 Q 版默认形象，皮肤包尚未纳入。捣蛋鬼目前按源码运行，解压后手动放置到 `public/models/`；应用内下载尚未接入。

每个文件的路径、大小和用途见 [FILES-trickster.md](FILES-trickster.md)。

## 校验

App 从 Release 下载 zip 后，按对应的 `<pet>.json` 校验整包 SHA-256、文件清单和逐文件哈希，通过后才解压。仓库不重复提交 zip，只保留插件定义与说明。
