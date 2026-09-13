#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 CloudRunFilesBuilder 的 latest release 同步 .run 文件到本仓库内嵌 store/run/ 目录,
然后把每个 .run 自解压包里的 .ipk 解压到应用同名子目录(软件包目录)——
store 中的所有文件均来源于 passengerya/CloudRunFilesBuilder。

.run 分类规则:
  - 文件名含 x86_64 / x86-64          -> store/run/x86/
  - 文件名含 aarch64 / arm64           -> store/run/arm64/
  - 文件名含 aarch32 / arm32 / i386    -> 跳过
  - 无架构标记(如 *_all.run、luci-app-uninstall-*.run) -> 同时放入 x86 和 arm64

同一应用同一架构存在多个资产时(例如 cortex-a53 与 generic 两个变体):
  - 优先保留本仓库现有文件使用的变体(不改变现有设备的安装习惯)
  - 本仓库没有该应用时, 新应用按 ARM64_VARIANT_PRIORITY 的顺序选择

24/25 通道分离:
  - 24.10 ipk 通道(前缀 24_/24- 或无前缀)与 25.12 apk 通道(前缀 25_/25-)
    各自独立选择变体, 两版 .run 在 store 中共存、互不挤占
  - 24 对应 shell/custom-packages.sh(opkg 构建), 25 对应 shell/apk-custom-packages.sh(apk 构建)

同步完成后, 删除同一应用、同一架构、同日期前缀下的旧版本 .run 文件
(24_ 只删 24_, 25- 只删 25-, 避免同步 apk 版时误删 ipk 版),
只清理 run/x86、run/arm64 根目录下的 .run。

软件包目录(.ipk)规则:
  - 每个 .run 解压出的 .ipk 放入以该 .run 推导出的应用同名子目录,
    如 dufs-0.46.0-r1_x86_64.run -> store/run/x86/dufs/*.ipk
  - 由本脚本解压生成的应用目录每次同步会重建(该目录归同步管理);
    人工新增 ipk 请放入独立的、与 .run 推导名不冲突的目录, 不会被删除
  - 不含 .ipk 的 .run(如 25.12 的 apk 包)不生成目录

用法:
  BUILDER_REPO=owner/repo GITHUB_TOKEN=xxx python3 store/sync_run_files.py
  --dry-run: 只打印将执行的操作, 不下载、不删除
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import urllib.error
import urllib.request

BUILDER_REPO = os.environ.get("BUILDER_REPO", "passengerya/CloudRunFilesBuilder").rstrip("/")
TOKEN = os.environ.get("GITHUB_TOKEN", "")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
RUN_DIR = os.path.join(ROOT, "store", "run")
ARCH_DIRS = {"x86": os.path.join(RUN_DIR, "x86"), "arm64": os.path.join(RUN_DIR, "arm64")}

# arm64 变体优先级(仅当本仓库中该应用没有既有文件时生效):
# generic 兼容性最好, 其次是 cortex-a53 优化构建、a53, 最后是纯 aarch64
ARM64_VARIANT_PRIORITY = ["generic", "cortex-a53", "a53", ""]

# 形如 "25-"/"24_" 的开头日期前缀(上游每日构建加在文件名前的标记)
RE_LEADING_PREFIX = re.compile(r"^\d{2}[-_]")
# 架构/变体标记(注意 aarch64 带变体的写法放在前面)
# 注意: all 必须带 _ 前缀且处于边界, 避免误删应用名内部的 "all"(如 passwall)
RE_ARCH = re.compile(r"_?(?:x86_64|x86-64|aarch64(?:_cortex-a53|_a53|_generic)?|aarch32|arm64)|_all(?=[-_.]|$)")
# 版本号: 可带 v 前缀的主版本 + 可选的 -r修订号(修订号后面必须是分隔符或结尾, 避免误吞 git hash)
RE_VERSION = re.compile(r"v?(\d+(?:\.\d+)+)(?:-r?(\d+)(?=[-_.]|$))?")
RE_REV = re.compile(r"r\d+")                 # 独立的 r9 之类修订标记
RE_HASH = re.compile(r"(?<![0-9a-z])[0-9a-f]{7,}(?![0-9a-z])")  # git 短 hash
RE_NUM = re.compile(r"(?<![0-9a-z])\d+(?![0-9a-z])")            # 独立数字(如 ssrp 的 196)
RE_ARCH_X86 = re.compile(r"x86_64|x86-64")
RE_ARCH_ARM64 = re.compile(r"aarch64|arm64")
RE_ARCH_ARM32 = re.compile(r"aarch32|arm32")
RE_ARCH_X8632 = re.compile(r"i386|x86_32")


def api_get(url):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "sync-run-files",
    }
    if TOKEN:
        headers["Authorization"] = "Bearer %s" % TOKEN
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def app_dir_of(name):
    """从 .run 文件名推导应用目录名(去掉前缀/架构/版本/修订/hash, 保留连字符, 小写)。"""
    s = name[:-4] if name.endswith(".run") else name
    s = RE_LEADING_PREFIX.sub("", s)
    s = RE_ARCH.sub("", s)
    s = RE_VERSION.sub("", s)
    s = RE_REV.sub("", s)
    s = RE_HASH.sub("", s)
    s = RE_NUM.sub("", s)
    return re.sub(r"[^0-9a-z-]+", "-", s.lower()).strip("-")


def channel_of(name):
    """返回通道: ipk(24.10, 前缀 24_/24- 或无前缀) 或 apk(25.12, 前缀 25_/25-)。

    24 对应 shell/custom-packages.sh(opkg/ipk 构建), 25 对应 shell/apk-custom-packages.sh(apk 构建),
    两版 .run 在 store 中按通道共存, 互不挤占。
    """
    m = RE_LEADING_PREFIX.match(name)
    if not m:
        return "ipk"
    return "apk" if m.group(0).startswith("25") else "ipk"


def norm_key(name):
    """从文件名提取应用标识(去掉前缀、架构、版本、hash, 统一小写)。"""
    s = name[:-4] if name.endswith(".run") else name
    s = RE_LEADING_PREFIX.sub("", s)
    s = RE_ARCH.sub("", s)
    s = RE_VERSION.sub("", s)
    s = RE_REV.sub("", s)
    s = RE_HASH.sub("", s)
    s = RE_NUM.sub("", s)
    return re.sub(r"[^0-9a-z]+", "_", s.lower()).strip("_")


def version_of(name):
    """解析版本用于排序, 返回 (主版本元组, 修订号), 没有版本返回 ((), 0)。"""
    s = name[:-4] if name.endswith(".run") else name
    s = RE_LEADING_PREFIX.sub("", s)
    m = RE_VERSION.search(s)
    if m:
        main = tuple(int(p) for p in m.group(1).split("."))
        rev = int(m.group(2)) if m.group(2) else 0
        return (main, rev)
    m = re.search(r"(?:^|[-_])r(\d+)(?:[-_.]|$)", s)
    if m:
        return ((), int(m.group(1)))
    return ((), 0)


def variant_of(name):
    """返回 arm64 变体: generic / cortex-a53 / a53 / ""(纯 aarch64); 非 arm64 返回 None。"""
    if "cortex-a53" in name:
        return "cortex-a53"
    if "generic" in name:
        return "generic"
    if "_a53" in name or "-a53" in name:
        return "a53"
    if RE_ARCH_ARM64.search(name):
        return ""
    return None


def arch_of(name):
    """返回资产应放入的目录列表。"""
    if RE_ARCH_ARM32.search(name) or RE_ARCH_X8632.search(name):
        return ["skip"]
    if RE_ARCH_X86.search(name):
        return ["x86"]
    if RE_ARCH_ARM64.search(name):
        return ["arm64"]
    return ["x86", "arm64"]  # 架构无关, 两个目录都放


def choose(cands, key, arch, existing_variants):
    """同一(应用, 架构)的多个候选里选一个。"""
    existing = existing_variants.get((key, arch))

    def sel(a):
        name = a["name"]
        variant = variant_of(name)
        m = RE_LEADING_PREFIX.match(name)
        prefix = int(m.group(0)[:2]) if m else -1
        keep_variant = (variant == existing) if existing is not None else False
        if arch == "arm64" and variant is not None:
            prio = ARM64_VARIANT_PRIORITY.index(variant)
        else:
            prio = 0
        return (
            version_of(name),   # 1. 版本高者优先
            keep_variant,       # 2. 优先保留本仓库现有变体
            not m,              # 3. 优先无日期前缀的命名(与仓库现有风格一致)
            prefix,             # 4. 有前缀时取日期较新者
            -prio,              # 5. 新应用按变体优先级
        )

    return sorted(cands, key=sel, reverse=True)[0]


def download_asset(asset, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    out = os.path.join(dest_dir, asset["name"])
    if os.path.isfile(out) and os.path.getsize(out) == asset.get("size", 0):
        print("[%s] 已存在且大小一致, 跳过下载: %s" % (os.path.basename(dest_dir), asset["name"]))
        return
    print("[%s] 下载 %s" % (os.path.basename(dest_dir), asset["name"]))
    headers = {"User-Agent": "sync-run-files"}
    if TOKEN:
        headers["Authorization"] = "Bearer %s" % TOKEN
    req = urllib.request.Request(asset["browser_download_url"], headers=headers)
    tmp = out + ".tmp"
    with urllib.request.urlopen(req, timeout=300) as resp, open(tmp, "wb") as f:
        shutil.copyfileobj(resp, f)
    if os.path.getsize(tmp) == 0:
        os.remove(tmp)
        raise RuntimeError("下载失败(空文件): %s" % asset["name"])
    os.replace(tmp, out)


def leading_prefix(name):
    """返回文件名开头的日期前缀(如 24_ / 25-), 无前缀返回空串。"""
    m = RE_LEADING_PREFIX.match(name)
    return m.group(0) if m else ""


def cleanup_old(key, arch, keep_name, dry_run=False):
    """删除 run/<arch>/ 根目录下同应用旧版本的 .run 文件(不触碰 .ipk 和子目录)。

    只清理与 keep_name 同前缀的旧文件(24_ 只删 24_, 25- 只删 25-),
    避免同步 apk 版(25_)时误删 ipk 版(24_)。
    """
    keep_prefix = leading_prefix(keep_name)
    d = ARCH_DIRS[arch]
    if not os.path.isdir(d):
        return
    for f in sorted(os.listdir(d)):
        p = os.path.join(d, f)
        if not f.endswith(".run") or f == keep_name or not os.path.isfile(p):
            continue
        if leading_prefix(f) != keep_prefix:
            continue
        if norm_key(f) == key:
            print("[%s] %s: %s" % (arch, "将删除" if dry_run else "删除旧版本", f))
            if not dry_run:
                os.remove(p)


def extract_ipks_from_runs(dry_run=False):
    """把 store/run/<arch>/ 根目录下每个 .run 解压出的 .ipk 放入应用同名子目录。

    来源即 CloudRunFilesBuilder 拉取的 .run 包本身(store 中所有文件均来源于 builder);
    解压生成的应用目录每次同步会重建, 不含 .ipk 的 .run(如 25.12 apk 包)不生成目录。
    """
    print("== 开始从 .run 解压 ipk 到应用子目录(软件包目录) ==")
    count = 0
    for arch, d in sorted(ARCH_DIRS.items()):
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            p = os.path.join(d, f)
            if not f.endswith(".run") or not os.path.isfile(p):
                continue
            app = app_dir_of(f)
            if not app:
                print("[%s] 无法推导应用名, 跳过: %s" % (arch, f))
                continue
            tmp = os.path.join(d, ".unpack-" + app)
            try:
                result = subprocess.run(
                    ["sh", p, "--target", tmp, "--noexec"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
                if result.returncode != 0:
                    print("[%s] 解压失败(返回码 %s), 跳过: %s" % (arch, result.returncode, f))
                    continue
                ipks = []
                for root, _, names in os.walk(tmp):
                    for n in names:
                        if n.endswith(".ipk"):
                            ipks.append(os.path.join(root, n))
                if not ipks:
                    print("[%s] 不含 ipk(apk 包或空包), 跳过: %s" % (arch, f))
                    continue
                dest = os.path.join(d, app)
                if dry_run:
                    print("[%s] %s -> %s/ (%d 个 ipk)" % (arch, f, app, len(ipks)))
                    count += len(ipks)
                    continue
                if os.path.isdir(dest):
                    shutil.rmtree(dest)
                os.makedirs(dest)
                for src in ipks:
                    shutil.copy2(src, dest)
                    print("[%s] ipk 解压: %s/%s" % (arch, app, os.path.basename(src)))
                    count += 1
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
    print("ipk 解压结束, 共处理 %d 个文件。" % count)


def main():
    parser = argparse.ArgumentParser(description="同步 run/ipk 文件到内嵌 store")
    parser.add_argument("--dry-run", action="store_true", help="只打印将执行的操作, 不下载、不删除")
    args = parser.parse_args()

    try:
        releases = api_get("https://api.github.com/repos/%s/releases?per_page=1" % BUILDER_REPO)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("源仓库 %s 暂无 release, 跳过 run 同步。" % BUILDER_REPO)
        else:
            raise
    else:
        if not releases:
            print("源仓库 %s 暂无 release, 跳过 run 同步。" % BUILDER_REPO)
        else:
            release = releases[0]
            print("使用 release: %s (%s)" % (release["tag_name"], release.get("name", "")))

            assets = [a for a in release.get("assets", []) if a["name"].endswith(".run")]
            if not assets:
                print("该 release 中没有 .run 资产, 跳过 run 同步。")
            else:
                run_sync(assets, args.dry_run)

    # ipk 阶段独立执行: 即使上游暂无新 .run 资产, 也要保持软件包目录与 .run 一致
    extract_ipks_from_runs(dry_run=args.dry_run)

    print("同步完成。" if not args.dry_run else "dry-run 结束, 未做任何修改。")


def run_sync(assets, dry_run=False):
    """从 CloudRunFilesBuilder Release 同步 .run 资产到内嵌 store(原有逻辑)。"""
    # 统计本仓库现有的变体选择(用于同名应用延续原变体)
    existing_variants = {}
    for arch, d in ARCH_DIRS.items():
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if f.endswith(".run"):
                v = variant_of(f)
                if v is not None:
                    existing_variants[(norm_key(f), arch)] = v

    # 按(通道, 应用, 架构)分组: 24/25 两个通道各自保留一个变体, 互不挤占
    groups = {}
    for a in assets:
        for arch in arch_of(a["name"]):
            if arch == "skip":
                print("跳过(架构不支持): %s" % a["name"])
                continue
            groups.setdefault((channel_of(a["name"]), norm_key(a["name"]), arch), []).append(a)

    for (channel, key, arch) in sorted(groups):
        cands = groups[(channel, key, arch)]
        chosen = choose(cands, key, arch, existing_variants)
        if len(cands) > 1:
            for c in cands:
                mark = "  <- 选中" if c is chosen else ""
                print("[%s] 候选: %s%s" % (arch, c["name"], mark))
        print("[%s] 同步: %s" % (arch, chosen["name"]))
        if dry_run:
            cleanup_old(key, arch, chosen["name"], dry_run=True)
            continue
        download_asset(chosen, ARCH_DIRS[arch])
        cleanup_old(key, arch, chosen["name"])


if __name__ == "__main__":
    main()
