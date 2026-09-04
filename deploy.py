# -*- coding: utf-8 -*-
"""一键发布：内联 manifest → 同步部署包 → 上传 Cloudflare → 提交推送 GitHub。

用法：
    python deploy.py                 全流程跑一遍
    python deploy.py -m "修复听辨选项布局"   自定义提交信息
    python deploy.py --no-push       只上线，不碰 git
    python deploy.py --no-deploy     只提交推送，不上线
    python deploy.py --no-inline     跳过内联（换题库时才需要重跑，平时可省）
    python deploy.py --dry-run       干跑，只打印要做什么，不真执行

设计原则：
    每一步单独校验，失败立刻停，绝不带着半成品往下走。
    先上线还是先推送可以分开，出问题范围最小。
"""
import argparse
import io
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.join(ROOT, "_app")
MANIFEST = os.path.join(ROOT, "audio", "manifest.json")
CF_PROJECT = "cabin-english-trainer"
CF_BRANCH = "main"


def sh(cmd, dry=False, check=True, retries=1):
    """跑一条命令。dry=True 时只打印。retries>1 时失败自动重试。"""
    print("    $ %s" % cmd)
    if dry:
        return ""
    last = ""
    for attempt in range(1, retries + 1):
        p = subprocess.run(cmd, shell=True, cwd=ROOT,
                           capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        last = (p.stdout or "") + (p.stderr or "")
        if p.returncode == 0:
            return last
        if attempt < retries:
            print("    失败，第 %d/%d 次重试..." % (attempt, retries))
    if check:
        print(last.strip())
        raise SystemExit("[中断] 命令执行失败，流程已停止，线上未被改动")
    return last


def step(n, total, title):
    print("\n[%d/%d] %s" % (n, total, title))


def read_version():
    """从 index.html 里读出 APP_VERSION，用作默认提交信息。"""
    path = os.path.join(ROOT, "index.html")
    if not os.path.exists(path):
        return None
    txt = io.open(path, encoding="utf-8", errors="replace").read()
    m = re.search(r'APP_VERSION\s*=\s*["\']([^"\']+)["\']', txt)
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser(description="公务英语AI陪练 - 一键发布")
    ap.add_argument("-m", "--message", help="git 提交信息")
    ap.add_argument("--no-inline", action="store_true", help="跳过 manifest 内联")
    ap.add_argument("--no-deploy", action="store_true", help="不上传 Cloudflare")
    ap.add_argument("--no-push", action="store_true", help="不提交推送 GitHub")
    ap.add_argument("--dry-run", action="store_true", help="只打印不执行")
    args = ap.parse_args()

    print("=" * 54)
    print("公务英语AI陪练 · 一键发布")
    print("项目目录: %s" % ROOT)
    print("=" * 54)

    # ---------- 前置检查 ----------
    print("\n[检查] 前置条件")
    for name, path in (("index.html", os.path.join(ROOT, "index.html")),
                       ("data.js", os.path.join(ROOT, "data.js")),
                       ("audio/manifest.json", MANIFEST)):
        if not os.path.exists(path):
            raise SystemExit("[中断] 缺少 %s，检查是不是进错目录了" % name)
        print("    OK  %s" % name)

    if not args.no_deploy:
        p = subprocess.run("wrangler --version", shell=True, cwd=ROOT,
                           capture_output=True, text=True)
        if p.returncode != 0:
            raise SystemExit("[中断] wrangler 不可用，先装：npm i -g wrangler")
        print("    OK  wrangler %s" % ((p.stdout or "").strip().splitlines() or ["?"])[0])

    ver = read_version()
    if ver:
        print("    应用版本: %s" % ver)

    total = sum([not args.no_inline, not args.no_deploy, not args.no_push]) + 1
    cur = 0

    # ---------- 1. 内联 manifest ----------
    if not args.no_inline:
        cur += 1
        step(cur, total, "内联 manifest 进 index.html")
        if os.path.exists(os.path.join(ROOT, "inline_manifest.py")):
            sh("python inline_manifest.py", dry=args.dry_run)
            print("    完成")
        else:
            print("    跳过（没找到 inline_manifest.py）")

    # ---------- 2. 同步部署包 ----------
    cur += 1
    step(cur, total, "同步部署包 -> _app/")
    if os.path.exists(os.path.join(ROOT, "sync_app.py")):
        out = sh("python sync_app.py", dry=args.dry_run)
        if out.strip():
            for line in out.strip().splitlines():
                print("    %s" % line)
    else:
        raise SystemExit("[中断] 没找到 sync_app.py，无法生成部署包")

    if not args.dry_run:
        for f in ("index.html", "data.js"):
            fp = os.path.join(APP_DIR, f)
            if not os.path.exists(fp):
                raise SystemExit("[中断] 部署包缺少 %s，同步有问题" % f)
            print("    OK  _app/%s (%d 字节)" % (f, os.path.getsize(fp)))

    # ---------- 3. 上传 Cloudflare ----------
    if not args.no_deploy:
        cur += 1
        step(cur, total, "上传 Cloudflare Pages")
        sh("wrangler pages deploy _app --project-name=%s --branch=%s"
           % (CF_PROJECT, CF_BRANCH), dry=args.dry_run)
        print("    完成")

    # ---------- 4. 提交推送 ----------
    if not args.no_push:
        cur += 1
        step(cur, total, "提交并推送 GitHub")

        msg = args.message
        if not msg:
            dirty = sh("git status --porcelain", dry=False, check=False).strip()
            if not dirty:
                print("    没有改动，跳过提交")
                print("\n" + "=" * 54)
                print("全部完成（无代码改动）")
                print("=" * 54)
                return
            msg = "%s 更新" % (ver or "更新")

        sh('git add -A', dry=args.dry_run)
        sh('git commit -m "%s"' % msg, dry=args.dry_run)
        out = sh("git push origin main", dry=args.dry_run, retries=3)
        if out and not args.dry_run:
            for line in out.strip().splitlines()[-3:]:
                print("    %s" % line)
        print("    完成")

    print("\n" + "=" * 54)
    print("全部完成")
    if not args.no_deploy:
        print("线上地址: https://en.boluomate.com")
    print("=" * 54)


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if e.code:
            print("\n%s" % e.code)
        sys.exit(1 if e.code else 0)
