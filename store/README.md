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

同步分两个阶段（`sync_run_files.py`）：

**阶段一：.run 文件**
- 来源：`passengerya/CloudRunFilesBuilder` 的**最新 Release**（每日构建的 .run 资产）
- 分类规则：
  - 文件名含 `x86_64` → `run/x86/`；含 `aarch64`/`arm64` → `run/arm64/`
  - 含 `aarch32`/`arm32`/`i386` → 跳过；无架构标记（如 `_all`）→ 两个目录都放
  - 同一应用同一架构多个变体时：优先延续现有变体；新应用按 `generic > cortex-a53 > a53 > 纯aarch64` 选择
  - 同步后删除**同应用、同架构、同日期前缀**的旧版本 .run（`24_` 只删 `24_`、`25-` 只删 `25-`），不触碰 .ipk 和子目录

**阶段二：软件包目录（.ipk 文件）**
- 来源：阶段一从 CloudRunFilesBuilder 拉取的 **.run 自解压包本身**——同步时把每个 .run 里的 .ipk 解压到应用同名子目录（如 `dufs-0.46.0-r1_x86_64.run` → `run/x86/dufs/*.ipk`）
- 由解压生成的应用目录每次同步会**重建**（归同步管理）；不含 .ipk 的 .run（如 25.12 的 apk 包）不生成目录
- 人工新增 ipk 请放入独立的、与 .run 推导名不冲突的目录，不会被删除

**触发**：`.github/workflows/sync-store.yml`
- 定时：每天 23:00 UTC（北京时间 7:00，晚于上游 6:00 的每日构建）
- 手动：workflow_dispatch（可指定其它源仓库）

> 本目录只由 `sync-store` 工作流自动更新，**不要手动修改**；如需人工新增 ipk，按应用建同名子目录放入即可。

## 如何手动同步

```bash
python3 store/sync_run_files.py --dry-run   # 预览
python3 store/sync_run_files.py             # 正式同步（需要 GITHUB_TOKEN）
```

<!-- AUTO-SOFTWARE-TABLE:START (Sync Store 自动维护, 勿手动修改) -->
| 软件 | 通道 | 版本 | 架构 | 包含软件包 |
| --- | --- | --- | --- | --- |
| argon | apk (25.12) | 2.4.7 | arm64 / x86 | luci-app-argon-config-26.236.50544~cb5d434.apk, luci-i18n-argon-config-zh-cn-26.236.50544~cb5d434.apk, luci-theme-argon-2.4.7-r20260824.apk |
| clashoo | apk (25.12) | 2026.09.14 | arm64 / x86 | clashoo-2026.09.14.dc66a8a-r1-aarch64_generic.apk, clashoo-2026.09.14.dc66a8a-r1-x86_64.apk, luci-app-clashoo-1.30.0-r14-aarch64_cortex-a53.apk, luci-i18n-cl... |
| easytier | apk (25.12) | v2.6.4 | arm64 / x86 | easytier-2.6.4.apk, easytier-noweb-2.6.4.apk, luci-app-easytier-2.6.4-r1.apk, luci-i18n-easytier-zh-cn-26.136.03667~39d7eda.apk |
| luci-app-advancedplus | apk (25.12) | 1.8.7-r20251116 | arm64 / x86 | luci-app-advancedplus-1.8.7-r20251116.apk, luci-i18n-advancedplus-zh-cn-0.apk |
| luci-app-amlogic | apk (25.12) | 3.1.321-r1 | arm64 / x86 | luci-app-amlogic-3.1.321-r1.apk, luci-i18n-amlogic-zh-cn-0.apk |
| luci-app-store | apk (25.12) | 0.2.1-r1 | arm64 / x86 | luci-app-store-0.2.1-r1.apk, luci-lib-taskd-1.0.26.apk, luci-lib-xterm-4.18.0.apk, taskd-1.0.3-r2.apk |
| luci-app-tailscale-community | apk (25.12) | 4.2.3-r1 | arm64 / x86 | luci-app-tailscale-community-4.2.3-r1.apk, luci-i18n-tailscale-community-zh-cn-0.260809.33933.apk |
| luci-theme-aurora | apk (25.12) | 1.3.0-r20260830 | arm64 / x86 | luci-theme-aurora-1.3.0-r20260830.apk |
| mosdns | apk (25.12) | v5.3.4-r14 | arm64 / x86 | geo2txt-1.0.0-r1.apk, luci-app-mosdns-1.7.14-r1.apk, luci-i18n-mosdns-zh-cn-26.255.53985~73981c0.apk, mosdns-5.3.4-r14.apk, v2ray-geoip-2026.09.12-r1.apk, v2... |
| openclash | apk (25.12) | v0.47.156 | arm64 / x86 | luci-app-openclash-0.47.156.apk |
| openwrt-daede | apk (25.12) | 2026.09.14 | arm64 / x86 | dae-2026.09.06-r2-aarch64_generic.apk, dae-2026.09.06-r2-x86_64.apk, daed-2026.09.06-r3-aarch64_generic.apk, daed-2026.09.06-r3-x86_64.apk, luci-app-daede-1.... |
| passwall | apk (25.12) | 26.9.9 | arm64 / x86 | chinadns-ng-2025.08.09-r1.apk, dns2socks-2.1-r2.apk, geoview-0.2.6-r1.apk, hysteria-2.12.2-r1.apk, luci-app-passwall-26.9.9-r1.apk, luci-i18n-passwall-zh-cn-... |
| passwall2 | apk (25.12) | 26.9.12-2 | arm64 / x86 | chinadns-ng-2025.08.09-r1.apk, geoview-0.2.6-r1.apk, luci-app-passwall2.apk, luci-i18n-passwall2-zh-cn.apk, shadowsocks-rust-sslocal-1.25.0-r1.apk, shadowsoc... |
| quickfile | apk (25.12) | 1.0.16 | arm64 / x86 | luci-app-quickfile-1.0.0-r1-aarch64_generic.apk, luci-app-quickfile-1.0.0-r1-x86_64.apk, luci-i18n-quickfile-zh-cn-26.143.10947.48a92b8-aarch64_generic.apk, ... |
| rtp2httpd | apk (25.12) | 3.17.1-r1 | arm64 / x86 | luci-app-rtp2httpd-3.17.1-r1.apk, luci-i18n-rtp2httpd-zh-cn-3.17.1.apk, rtp2httpd-3.17.1-r1_aarch64_generic.apk, rtp2httpd-3.17.1-r1_x86_64.apk |
| sing-box | apk (25.12) | v1.14.0 | arm64 / x86 | sing-box_1.14.0_openwrt_aarch64_generic.apk, sing-box_1.14.0_openwrt_x86_64.apk |
| ssrp-mihomo | apk (25.12) |  | arm64 / x86 | chinadns-ng-2025.08.09-r1.apk, dns2tcp-1.1.2-r1.apk, ipt2socks-1.1.4-r3.apk, lua-neturl-1.2.1-r1.apk, luci-app-ssr-plus-196-r9.apk, luci-i18n-ssr-plus-zh-cn-... |
| adguardhome | ipk (24.10) | v0.107.79 | arm64 / x86 | luci-app-adguardhome-all.ipk |
| argon | ipk (24.10) | 2.4.3-r20250722 | arm64 / x86 | luci-app-argon-config_26.126.28706-6ac4a03_all.ipk, luci-i18n-argon-config-zh-cn_26.126.28706-6ac4a03_all.ipk, luci-theme-argon_2.4.3-r20250722_all.ipk |
| bandix | ipk (24.10) | 0.11.0-r25 | arm64 / x86 | bandix_0.11.0-r25_aarch64_generic.ipk, bandix_0.11.0-r25_x86_64.ipk, luci-app-bandix_0.11.1-r38_all.ipk, luci-i18n-bandix-zh-cn_26.249.51071.0bd9b61_all.ipk |
| clashoo | ipk (24.10) | 2026.09.11 | arm64 / x86 | clashoo_2026.09.11.dca26db-r1_aarch64_cortex-a53.ipk, clashoo_2026.09.11.dca26db-r1_x86_64.ipk, luci-app-clashoo_1.30.0-r13_all.ipk, luci-i18n-clashoo-zh-cn_... |
| dufs | ipk (24.10) | 0.46.0-r1 | arm64 / x86 | dufs_0.46.0-r1_aarch64_generic.ipk, dufs_0.46.0-r1_x86_64.ipk, luci-app-dufs_26.126.28706-6ac4a03_all.ipk, luci-i18n-dufs-zh-cn_26.126.28706-6ac4a03_all.ipk |
| easytier | ipk (24.10) | v2.6.4 | arm64 / x86 | easytier-noweb_2.6.4_aarch64_generic.ipk, easytier-noweb_2.6.4_x86_64.ipk, easytier_2.6.4_aarch64_generic.ipk, easytier_2.6.4_x86_64.ipk, luci-app-easytier_2... |
| homeproxy | ipk (24.10) | 26.187.07809 | arm64 / x86 | luci-app-homeproxy_26.187.07809-9bce398_all.ipk, luci-i18n-homeproxy-zh-cn_26.126.28706-6ac4a03_all.ipk, sing-box-tiny_1.12.25-r1_aarch64_generic.ipk, sing-b... |
| luci-app-advancedplus | ipk (24.10) | 1.8.7-r20251116 | arm64 / x86 | luci-app-advancedplus_1.8.7-r20251116_all.ipk, luci-i18n-advancedplus-zh-cn_0_all.ipk |
| luci-app-amlogic | ipk (24.10) | 3.1.321-r1 | arm64 / x86 | luci-app-amlogic_3.1.321-r1_all.ipk, luci-i18n-amlogic-zh-cn_0_all.ipk |
| luci-app-nekobox | ipk (24.10) | 2.0.9 | arm64 / x86 | luci-app-nekobox_2.0.9-rc14_all.ipk |
| luci-app-store | ipk (24.10) | 0.2.1-r1 | arm64 / x86 | luci-app-store_0.2.1-r1_all.ipk, luci-lib-taskd_1.0.26_all.ipk, luci-lib-xterm_4.18.0_all.ipk, taskd_1.0.3-2_all.ipk |
| luci-app-tailscale-community | ipk (24.10) | 4.2.3-r1 | arm64 / x86 | luci-app-tailscale-community_4.2.3-r1_all.ipk, luci-i18n-tailscale-community-zh-cn_0.260809.33932_all.ipk |
| luci-app-uninstall | ipk (24.10) | v1.2.6 | arm64 / x86 | luci-app-uninstall_1.2.6_all.ipk |
| luci-theme-aurora | ipk (24.10) | 1.3.0-r20260830 | arm64 / x86 | luci-theme-aurora_1.3.0-r20260830_all.ipk |
| lucky | ipk (24.10) | 2.20.2-r13 | arm64 / x86 | luci-app-lucky_3.0.2-r15_all.ipk, lucky_2.20.2-r13_aarch64_generic.ipk, lucky_2.20.2-r13_x86_64.ipk |
| momo | ipk (24.10) | v1.2.1 | arm64 / x86 | luci-app-momo_1.2.1-r1_all.ipk, luci-i18n-momo-zh-cn_26.154.52640dc0b315_all.ipk, momo_2026.06.03-r1_aarch64_cortex-a53.ipk, momo_2026.06.03-r1_x86_64.ipk |
| mosdns | ipk (24.10) | v5.3.4-r14 | arm64 / x86 | geo2txt_1.0.0-r1_aarch64_cortex-a53.ipk, geo2txt_1.0.0-r1_x86_64.ipk, luci-app-mosdns_1.7.14-r1_all.ipk, luci-i18n-mosdns-zh-cn_26.255.5398573981c0_all.ipk, ... |
| nikki | ipk (24.10) | v1.26.1 | arm64 / x86 | luci-app-nikki_1.26.1-r1_all.ipk, luci-i18n-nikki-ru_26.161.5655095d41dd_all.ipk, luci-i18n-nikki-zh-cn_26.161.5655095d41dd_all.ipk, luci-i18n-nikki-zh-tw_26... |
| openclash | ipk (24.10) | v0.47.156 | arm64 / x86 | luci-app-openclash_0.47.156_all.ipk |
| openlist2 | ipk (24.10) | v4.2.6 | arm64 / x86 | luci-app-openlist2_1.0.3-r1_all.ipk, luci-i18n-openlist2-zh-cn_26.210.29779a90fc2a_all.ipk, openlist2_4.2.6-r1_aarch64_cortex-a53.ipk, openlist2_4.2.6-r1_x86... |
| openwrt-daede | ipk (24.10) | 2026.09.13 | arm64 / x86 | dae_2026.09.06-r2_aarch64_generic.ipk, dae_2026.09.06-r2_x86_64.ipk, daed_2026.09.06-r3_aarch64_generic.ipk, daed_2026.09.06-r3_x86_64.ipk, luci-app-daede_1.... |
| passwall | ipk (24.10) | 26.9.9-1 | arm64 / x86 | 23.05-24.10_luci-app-passwall_26.9.9-r1_all.ipk, 23.05-24.10_luci-i18n-passwall-zh-cn_26.9.9_all.ipk, chinadns-ng_2025.08.09-r1_aarch64_cortex-a53.ipk, china... |
| passwall2 | ipk (24.10) | 26.9.12-2 | arm64 / x86 | chinadns-ng_2025.08.09-r1_aarch64_cortex-a53.ipk, chinadns-ng_2025.08.09-r1_x86_64.ipk, geoview_0.2.3-r1_aarch64_cortex-a53.ipk, geoview_0.2.3-r1_x86_64.ipk,... |
| quickfile | ipk (24.10) | 1.0.16 | arm64 / x86 | luci-app-quickfile_1.0.0-r1_all.ipk, luci-i18n-quickfile-zh-cn_26.143.10947.48a92b8_all.ipk, quickfile_1.0.16-r1_aarch64_generic.ipk, quickfile_1.0.16-r1_x86... |
| rtp2httpd | ipk (24.10) | 3.17.1-r1 | arm64 / x86 | luci-app-rtp2httpd_3.17.1-r1_all.ipk, luci-i18n-rtp2httpd-zh-cn_3.17.1_all.ipk, rtp2httpd_3.17.1-r1_aarch64_generic.ipk, rtp2httpd_3.17.1-r1_x86_64.ipk |
| sing-box | ipk (24.10) | v1.14.0 | arm64 / x86 | sing-box_1.14.0_openwrt_aarch64_generic.ipk, sing-box_1.14.0_openwrt_x86_64.ipk |
| ssrp-mihomo | ipk (24.10) |  | arm64 / x86 | chinadns-ng_2025.08.09-r1_aarch64_cortex-a53.ipk, chinadns-ng_2025.08.09-r1_x86_64.ipk, dns2socks-rust_0.2.6-r4_aarch64_cortex-a53.ipk, dns2socks-rust_0.2.6-... |
<!-- AUTO-SOFTWARE-TABLE:END -->
