# Arknights 桌宠档案库

`Arknights-Desktop-Pets-Archive`

> **本仓库不是开源素材库。**
>
> Release 中分发的 Spine 模型、贴图、语音与角色图标，版权归上海鹰角网络有限公司所有。
> 本仓库不授予任何许可证，也不代表鹰角网络的授权或认可。
> 素材仅供个人非商业使用，不得用于商业用途，不得损害版权方利益。

## 这是什么

JNGKZbird 的桌宠项目配套素材档案库。第一个接入的是**予愿安洁莉娜桌宠**；捣蛋鬼桌宠实装后，会以新的 pet 条目加入同一仓库。

本仓库服务于作者的多个桌宠项目，不单独发布桌宠产品。代码仓库采用 MIT 许可证，但游戏素材不适用 MIT；为了让代码与素材的授权边界清楚，素材从代码仓库中剥离，单独归档在这里。

本仓库只保存：

- 各宠物、各平台的素材打包脚本；
- manifest（宠物、版本、文件清单、SHA-256）；
- 版权与使用说明。

素材压缩包通过 **GitHub Releases** 分发，不提交进 Git 历史，也不使用网盘。

> **仓库名已定**：`Arknights-Desktop-Pets-Archive`。它是作者其他桌宠项目的配套仓库，后续新增宠物直接扩展 `PET_SPECS`，不另开素材库。

## 目录结构

```text
windows/<pet>.json            # Windows 插件定义
windows/README.md             # Windows 素材包说明
harmonyos/<pet>.json          # HarmonyOS 插件定义
harmonyos/README.md           # HarmonyOS 素材包说明
android/<pet>.json            # Android 插件定义
android/README.md             # Android 素材包说明
tools/build_packages.py       # 打包脚本
dist/<pet>/<platform>.zip     # 构建产物，gitignored，发布到 Releases
```

仓库不提交 zip，避免重复 Git 内容；每个平台文件夹里只放插件定义和对应 zip 的说明，素材包本体在 Releases。

每个平台目录另有 `FILES.md`：从 `angelina.json` 自动生成的逐文件清单（路径、大小、用途）。

## 仓库文件说明

| 路径 | 内容 |
|---|---|
| `windows/` | Windows 插件定义 `angelina.json`、`README.md`、逐文件清单 `FILES.md` |
| `harmonyos/` | HarmonyOS 插件定义与同构说明 |
| `android/` | Android 插件定义与同构说明 |
| `tools/build_packages.py` | 从本地素材源构建三平台 zip 与插件定义 |
| `tools/build_file_docs.py` | 从插件定义生成各平台 `FILES.md` |
| `.gitignore` | 忽略 `dist/`、zip、缓存文件 |
| `NOTICE.md` | 素材版权声明 |
| `README.md` | 仓库总说明 |

当前宠物：

| pet | 名称 | 状态 |
|---|---|---|
| `angelina` | 予愿安洁莉娜 | 已接入 |
| `trickster` | 捣蛋鬼桌宠 | 预留，实装后接入 |

## 发布包

| 平台 | 发布文件 | 内容（angelina） |
|---|---|---|
| Windows | `windows.zip` | `pets/予愿安洁莉娜/{spine,voice_cn,voice_jp}`、`pets/技能图标`、`assets/avatar.png` |
| HarmonyOS | `harmonyos.zip` | `spine`、`voice`、`voice_jp`、`avatar.png`，解压到 `filesDir/plugins/angelina/<版本>/` |
| Android | `android.zip` | `spine`、`voice`、`voice_jp`，解压到 `filesDir/plugins/angelina/<版本>/` |

角色 Skill 文本留在代码仓库，按 CC BY-NC-SA 4.0 分发，不在这些素材包内。

Release tag 约定为 `<pet>-assets-v<主版本>`，例如 `angelina-assets-v1`。下载地址：

```text
https://github.com/JNGKZbird/Arknights-Desktop-Pets-Archive/releases/download/<pet>-assets-v<N>/<platform>.zip
```

## 下载与安装

1. 打开本仓库的 **Releases**，选择对应宠物的 tag。
2. 下载对应平台的 zip。
3. 软件首次启动时会提示下载；也可以手动下载后，在软件中选择“手动导入官方 zip”。

手动导入只接受与本仓库 Release 中**完全一致**的官方 zip：整包 SHA-256 必须匹配，随后还会校验文件清单与逐文件哈希。其他宠物、旧版本、修改过的包，或重新压缩导致字节变化的包都会被拒绝。请直接使用 Release 里的原始文件。

## 构建

构建脚本读取本机已有的素材目录，生成 zip 和 manifest：

```bash
python tools/build_packages.py --pet angelina --platform windows
python tools/build_packages.py --pet angelina --platform harmonyos
python tools/build_packages.py --pet angelina --platform android
python tools/build_file_docs.py --pet angelina
```

修改插件定义或素材后，重新生成各平台的 `FILES.md`。

默认源目录：

- Windows：`D:\Angelina-pet-芋圆-windows版`
- HarmonyOS：`D:\Arknights-Angelina-pet`
- Android：`D:\Angelina-pet-芋圆-安卓版`

可用 `--windows-root`、`--harmonyos-root`、`--android-root` 覆盖；新宠物在 `PET_SPECS` 中新增条目。生成的 zip 在 `dist/<pet>/`，插件定义在 `windows|harmonyos|android/<pet>.json`；zip 不提交 Git，发布到 Releases。

发布新版本时使用新的 tag（如 `angelina-assets-v2`），并同步更新各桌宠内置的 manifest。

## 版权与下架

素材版权归上海鹰角网络有限公司所有。本仓库不提供任何形式的授权或许可。

如权利方对本仓库有异议，请通过 GitHub Issues 联系仓库所有者；仓库所有者应停止分发并删除相关内容。

