# 软件支持列表

> 本文件仅作索引。实际软件清单由 Sync Store 工作流自动维护，请以清单文件为准。

本项目可集成的软件来自两个来源：

## 来源一：上游同步的第三方软件（每日自动同步）

由 [CloudRunFilesBuilder](https://github.com/passengerya/CloudRunFilesBuilder) 每日打包，Sync Store 工作流自动同步进本仓库内嵌 `store/`。

- **软件清单**：[store/README.md](store/README.md) 软件表（软件 | 中文名 | 通道 | 版本 | 架构 | 用途 | 来源），与内嵌 store 实际内容一致
- **软件开关**：`shell/custom-packages.sh`（24.10 ipk 通道）、`shell/apk-custom-packages.sh`（25.12 apk 通道）自动生成段
- **开启方式**：取消对应行的注释后触发构建；连续 3 次不在上游 Release 的软件会标记「⚠️上游停更」但保留
- **冲突提示**：冲突组（clashoo↔nikki、advancedplus↔argon、quickfile↔luci-app-run、argon↔shadcn）同时启用时同步脚本在生成段顶部输出 ⚠️ 警告；各机型 build 脚本固定加入 Argon，启用 shadcn 等备选主题（非纯 CSS 主题，会接管 LuCI 菜单/路由）会提示多主题并存
- **冗余包剔除**：`easytier-noweb`、`luci-i18n-easytier-zh-cn` 与主包文件冲突，同步时自动剔除，请勿手动加入

## 来源二：ImmortalWrt 官方仓库内软件（固定清单，无需同步）

固件底层来源就是 ImmortalWrt 官方仓库，这些软件构建时直接从官方源解析安装。

- **软件清单**：[store/imm-packages.md](store/imm-packages.md)（软件包 | 中文说明）
- **软件开关**：上述两个开关文件的「以下imm仓库内的软件」固定段（同步不触碰）
- **开启方式**：取消对应行的注释后触发构建
