#!/bin/bash
# ============= 第三方软件开关（24.10 ipk 通道） =============
# 本文件由 Sync Store 工作流自动维护（每天北京时间 7:00 更新），请勿手动修改。
# 选择软件：把对应软件行行首的 # 去掉（取消注释）即可；下次同步保持你的选择。
# 与 25.12 通道对应文件：shell/apk-custom-packages.sh
# ==========================================================

# ============ 以下由 Sync Store 自动维护(根据内嵌 store 实际内容生成) ============
# 自动生成: adguardhome | 本地DNS去广告 | AdGuardHome 广告拦截与 DNS 服务 | v0.107.79 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES luci-app-adguardhome-all"
# 自动生成: argon | Argon主题 | 简洁主题, 支持明暗自动切换 | 2.4.3-r20250722 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES luci-app-argon-config luci-i18n-argon-config-zh-cn luci-theme-argon"
# 自动生成: bandix | 流量监控 | Bandix 实时流量监控与统计 | 0.11.0-r25 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES bandix luci-app-bandix luci-i18n-bandix-zh-cn"
# 自动生成: clashoo | Clashoo代理 | 代理工具(与 nikki 冲突勿同时开启) | 2026.09.11 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES clashoo luci-app-clashoo luci-i18n-clashoo-zh-cn"
# 自动生成: dufs | 文件服务器 | 轻量文件服务器(静态托管/上传/WebDAV) | 0.46.0-r1 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES dufs luci-app-dufs luci-i18n-dufs-zh-cn"
# 自动生成: easytier | 异地组网 | EasyTier 点对点组网工具 | v2.6.4 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES easytier easytier-noweb luci-app-easytier luci-i18n-easytier-zh-cn"
# 自动生成: homeproxy | 代理平台 | 现代代理平台(基于 sing-box) | 26.187.07809 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES luci-app-homeproxy luci-i18n-homeproxy-zh-cn sing-box-tiny"
# 自动生成: luci-app-advancedplus | 高级设置 | 进阶设置(与 argon-config 冲突勿同时开启) | 1.8.7-r20251116 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES luci-app-advancedplus luci-i18n-advancedplus-zh-cn"
# 自动生成: luci-app-amlogic | 晶晨宝盒 | 晶晨机顶盒管理(仅 ARM64 平台) | 3.1.321-r1 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES luci-app-amlogic luci-i18n-amlogic-zh-cn"
# 自动生成: luci-app-nekobox | NekoBox代理 | NekoBox 代理工具 | 2.0.9 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES luci-app-nekobox"
# 自动生成: luci-app-store | iStore商店 | iStore 应用商店 | 0.2.1-r1 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES luci-app-store luci-lib-taskd luci-lib-xterm taskd"
# 自动生成: luci-app-tailscale-community | Tailscale组网 | Tailscale 组网(Community 版) | 4.2.3-r1 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES luci-app-tailscale-community luci-i18n-tailscale-community-zh-cn"
# 自动生成: luci-app-uninstall | 高级卸载 | 彻底卸载插件的工具 | v1.2.6 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES luci-app-uninstall"
# 自动生成: luci-theme-aurora | 极光主题 | 极光主题界面 | 1.3.0-r20260830 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES luci-theme-aurora"
# 自动生成: lucky | Lucky大吉 | 端口转发/反向代理/内网穿透 | 2.20.2-r13 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES luci-app-lucky lucky"
# 自动生成: momo | Momo代理 | 基于 sing-box 的透明代理 | v1.2.1 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES luci-app-momo luci-i18n-momo-zh-cn momo"
# 自动生成: mosdns | DNS分流 | 高性能 DNS 分流(DoH/DoQ 等) | v5.3.4-r14 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES geo2txt luci-app-mosdns luci-i18n-mosdns-zh-cn mosdns v2ray-geoip v2ray-geosite"
# 自动生成: nikki | Nikki代理 | 代理工具(与 clashoo 冲突勿同时开启) | v1.26.1 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES luci-app-nikki luci-i18n-nikki-ru luci-i18n-nikki-zh-cn luci-i18n-nikki-zh-tw mihomo-alpha mihomo-meta nikki"
# 自动生成: openclash | OpenClash | Clash 代理客户端 | v0.47.156 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES luci-app-openclash"
# 自动生成: openlist2 | 网盘聚合 | OpenList2 网盘聚合(Alist 变体) | v4.2.6 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES luci-app-openlist2 luci-i18n-openlist2-zh-cn openlist2"
# 自动生成: openwrt-daede | eBPF代理 | 基于 eBPF 的高性能透明代理(dae/daed) | 2026.09.13 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES dae daed luci-app-daede vmlinux-btf"
# 自动生成: passwall | PassWall | 代理工具(自带依赖) | 26.9.9-1 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES 23.05-24.10_luci-app-passwall 23.05-24.10_luci-i18n-passwall-zh-cn chinadns-ng dns2socks geoview ipt2socks microsocks naiveproxy shadow-tls shadowsocks-rust-sslocal shadowsocks-rust-ssserver shadowsocksr-libev-ssr-local shadowsocksr-libev-ssr-redir shadowsocksr-libev-ssr-server simple-obfs-client tcping trojan-plus tuic-client v2ray-geoip v2ray-geosite v2ray-plugin xray-core xray-plugin"
# 自动生成: passwall2 | PassWall2 | 代理工具(自带依赖) | 26.9.12-2 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES chinadns-ng geoview luci-app-passwall2 luci-i18n-passwall2-zh-cn naiveproxy shadowsocks-rust-sslocal shadowsocks-rust-ssserver shadowsocksr-libev-ssr-local shadowsocksr-libev-ssr-redir shadowsocksr-libev-ssr-server simple-obfs-client tcping tuic-client v2ray-geoip v2ray-geosite v2ray-plugin xray-core"
# 自动生成: quickfile | 文件管理 | 轻量网页文件管理器(与 luci-app-run 冲突勿同时开启) | 1.0.16 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES luci-app-quickfile luci-i18n-quickfile-zh-cn quickfile"
# 自动生成: rtp2httpd | IPTV转发 | IPTV 流媒体转发服务器 | 3.17.1-r1 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES luci-app-rtp2httpd luci-i18n-rtp2httpd-zh-cn rtp2httpd"
# 自动生成: sing-box | Sing-box内核 | 通用代理内核 | v1.14.0 | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES sing-box"
# 自动生成: ssrp-mihomo | SSRP代理 | SSR-Plus 代理工具(mihomo 内核) | | 取消下一行注释即启用
#CUSTOM_PACKAGES="$CUSTOM_PACKAGES chinadns-ng dns2socks dns2socks-rust dns2tcp hysteria ipt2socks ipt2socks-rs libopenssl3 libudns lua-neturl luci-app-ssr-plus luci-i18n-ssr-plus-zh-cn microsocks mosdns naiveproxy redsocks2 shadow-tls shadowsocks-libev-ss-server shadowsocks-rust-sslocal shadowsocks-rust-ssmanager shadowsocks-rust-ssserver shadowsocks-rust-ssservice shadowsocks-rust-ssurl shadowsocksr-libev-ssr-check shadowsocksr-libev-ssr-local shadowsocksr-libev-ssr-nat shadowsocksr-libev-ssr-redir shadowsocksr-libev-ssr-server simple-obfs-client tcping tcping-simple trojan trojan-plus tuic-client v2ray-plugin xray-core"
# ============ 自动维护结束 ============
