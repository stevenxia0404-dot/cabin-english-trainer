#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_audio.py —— 公务英语AI陪练 音频生成脚本

从 data.js 读取全部句子，用微软神经语音（edge-tts）合成 MP3 到 audio/，
并自动重写 audio/manifest.json。应用只认 manifest（句子文本 -> 音频文件），
不认句子本身，所以换资料时改 data.js + 重跑本脚本即可，代码零改动。

用法：
    python gen_audio.py            增量生成（已存在的音频跳过）
    python gen_audio.py --clean    生成后删除不在 manifest 里的孤儿 mp3
    python gen_audio.py --dry-run  只列出要生成的句子，不实际合成

依赖：pip install edge-tts
"""
import argparse
import asyncio
import hashlib
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_JS = os.path.join(ROOT, "data.js")
AUDIO_DIR = os.path.join(ROOT, "audio")
MANIFEST = os.path.join(AUDIO_DIR, "manifest.json")

# 音色（Steven 2026-09-01 试听后拍板）
#   男声 Brian = 考官：念单词考你、提问（w / q）
#   女声 Jenny = 标准示范：跟读短句、标准应答（s / a）
# 学员一听声音就能分清"这是在考我"还是"这是标准答案"。
VOICE_Q = "en-US-BrianNeural"
VOICE_A = "en-US-JennyNeural"
SLOW_RATE = "-50%"   # 慢速版：降速 50%

NODE = "node"


def extract_sentences():
    """用 Node 解析 data.js（JS 格式，key 无引号，不是纯 JSON）。
    返回 {"w":[单词], "s":[跟读短句], "q":[问题+换说法], "a":[应答]}"""
    js = r"""
const fs = require('fs');
const D = new Function(fs.readFileSync('data.js', 'utf8') + '; return DATA;')();
const w = [], s = [], q = [], a = [], m = [], seen = {};
const add = (arr, k, t) => { if (t && !seen[k + t]) { seen[k + t] = 1; arr.push(t); } };
D.scenes.forEach(sc => sc.pairs.forEach(p => {
  add(w, 'w', p.w);   // 第一关听辨：单词
  add(s, 's', p.s);   // 第二关跟读：短句
  add(q, 'q', p.q);   // 第三关：考官提问
  (p.variants || []).forEach(v => add(q, 'q', v));
  add(a, 'a', p.a);   // 第三关：标准应答
  (p.samples || []).forEach(x => add(m, 'm', x));
}));
process.stdout.write(JSON.stringify({ w, s, q, a, m }));
"""
    r = subprocess.run([NODE, "-e", js], cwd=ROOT, capture_output=True,
                       text=True, timeout=30)
    if r.returncode != 0:
        sys.exit(f"[错误] Node 解析 data.js 失败：{r.stderr.strip()}")
    return json.loads(r.stdout)


def filename(text, prefix):
    """稳定命名：按句子文本 md5 前 7 位。同一句永远同名 -> 增量、去重、好排查"""
    h = hashlib.md5(text.encode("utf-8")).hexdigest()[:7]
    return f"{prefix}_{h}.mp3"


def synth(text, voice, rate, out):
    """合成单个音频。返回 True=本次生成，False=文件已存在跳过"""
    if os.path.exists(out):
        return False
    try:
        import edge_tts
    except ImportError:
        sys.exit("[错误] 缺少 edge-tts，请先运行：pip install edge-tts")

    async def _run():
        await edge_tts.Communicate(text, voice, rate=rate).save(out)

    asyncio.run(_run())
    return True


def main():
    ap = argparse.ArgumentParser(description="公务英语AI陪练 音频生成脚本")
    ap.add_argument("--clean", action="store_true",
                    help="生成后删除 audio/ 里不在 manifest 中的孤儿 mp3")
    ap.add_argument("--dry-run", action="store_true",
                    help="只打印要生成的句子，不合成")
    args = ap.parse_args()

    os.makedirs(AUDIO_DIR, exist_ok=True)
    sents = extract_sentences()
    man = {"w": {}, "s": {}, "q": {}, "a": {}, "m": {}}
    made, skipped = 0, 0

    def handle(kind, text, voice, rate, prefix):
        nonlocal made, skipped
        f = filename(text, prefix)
        out = os.path.join(AUDIO_DIR, f)
        if args.dry_run:
            print(f"[dry-run] {kind} {f}  <-  {text}")
        elif synth(text, voice, rate, out):
            made += 1
            print(f"[生成] {f}  <-  {text[:50]}")
        else:
            skipped += 1
        return f

    # 单词：男声 Brian，只出正常版（第一关听辨）
    for t in sents["w"]:
        f = handle("w", t, VOICE_Q, "+0%", "w")
        man["w"][t] = f

    # 考官问题：男声，只出正常版（manifest 用字符串）
    for t in sents["q"]:
        f = handle("q", t, VOICE_Q, "+0%", "q")
        man["q"][t] = f

    # 跟读短句：女声 Jenny，正常 + 慢速（manifest 用 {n, s} 对象）
    for t in sents["s"]:
        fn = handle("s", t, VOICE_A, "+0%", "s")
        fs_ = handle("s_slow", t, VOICE_A, SLOW_RATE, "s_slow")
        man["s"][t] = {"n": fn, "s": fs_}

    # 员工应答：女声，正常 + 慢速（manifest 用 {n, s} 对象）
    for t in sents["a"]:
        fn = handle("a", t, VOICE_A, "+0%", "a")
        fs_ = handle("a_slow", t, VOICE_A, SLOW_RATE, "a_slow")
        man["a"][t] = {"n": fn, "s": fs_}

    for t in sents["m"]:
        f = handle("m", t, VOICE_A, "+0%", "m")
        man["m"][t] = f

    if args.dry_run:
        return

    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(man, f, ensure_ascii=False, indent=2)
    print(f"manifest 已写入 {MANIFEST} (w {len(man['w'])} / q {len(man['q'])} / s {len(man['s'])} / a {len(man['a'])} / m {len(man['m'])} 条)")
    print(f"本次生成 {made} 个，跳过已有 {skipped} 个")

    if args.clean:
        # 孤儿清理：manifest 引用的文件集合
        keep = set(man["q"].values())
        keep.update(man["w"].values())
        keep.update(man["m"].values())
        for e in man["s"].values():
            keep.add(e["n"]); keep.add(e["s"])
        for e in man["a"].values():
            keep.add(e["n"]); keep.add(e["s"])
        removed, failed = 0, 0
        for name in os.listdir(AUDIO_DIR):
            if name.endswith(".mp3") and name not in keep:
                try:
                    os.remove(os.path.join(AUDIO_DIR, name))
                    removed += 1
                except OSError:
                    failed += 1   # 沙箱里回收站不可用会抛异常，删不掉也不能让整个脚本崩掉
        msg = f"孤儿清理：删除 {removed} 个"
        if failed:
            msg += (f"，{failed} 个删不掉（沙箱回收站限制）—— 不影响功能："
                    f"manifest 不引用它们，部署时也只复制引用到的文件")
        print(msg)


if __name__ == "__main__":
    main()
