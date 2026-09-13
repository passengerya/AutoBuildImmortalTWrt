# 内嵌 store 目录

本目录存储 **ImmortalWrt 官方仓库以外**的第三方软件包（.run 自解压包 + .ipk），
供本项目各机型的构建脚本直接使用（构建时挂载到 ImageBuilder 容器内的
`/home/build/immortalwrt/store`，由 `shell/prepare-packages.sh` 解包收集到 `packages/` 目录）。

## 目录结构

```
store/
├── run/
│   ├── x86/      # x86_64 架构: .run 放根目录, .ipk 按应用建同名子目录
│   └── arm64/    # aarch64 架构: 同上
├── README.md
└── sync_run_files.py            # 同步脚本（由 sync-store 工作流调用）
```

## 同步机制

- 来源：`passengerya/CloudRunFilesBuilder` 的**最新 Release**（每日构建的 .run 资产）
- 触发：`.github/workflows/sync-store.yml`
  - 定时：每天 23:00 UTC（北京时间 7:00，晚于上游 6:00 的每日构建）
  - 手动：workflow_dispatch（可指定其它源仓库）
- 分类规则（`sync_run_files.py`）：
  - 文件名含 `x86_64` → `run/x86/`；含 `aarch64`/`arm64` → `run/arm64/`
  - 含 `aarch32`/`arm32`/`i386` → 跳过；无架构标记（如 `_all`）→ 两个目录都放
  - 同一应用同一架构多个变体时：优先延续现有变体；新应用按 `generic > cortex-a53 > a53 > 纯aarch64` 选择
  - 同步后删除**同应用、同架构、同日期前缀**的旧版本 .run（`24_` 只删 `24_`、`25-` 只删 `25-`），不触碰 .ipk 和子目录
- 本目录只由 `sync-store` 工作流自动更新，**不要手动修改**；如需人工新增 ipk，按应用建同名子目录放入即可（同步脚本不会删除 .ipk）

## 如何手动同步

```bash
python3 store/sync_run_files.py --dry-run   # 预览
python3 store/sync_run_files.py             # 正式同步（需要 GITHUB_TOKEN）
```
