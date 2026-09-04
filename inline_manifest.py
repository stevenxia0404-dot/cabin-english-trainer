"""把 audio/manifest.json 内联进 index.html，消除异步竞态。

背景：manifest 原先是 fetch("audio/manifest.json") 异步加载的，
而 speak() 查不到条目就会回退到手机系统合成音（Samantha）。
开屏头几秒 manifest 还没回来，此时播报全是合成音，
且到货前后音色不一致 —— 同一关里 Brian 和 Samantha 混着出现。
内联后随 HTML 同步到位，这个竞态从根上消失。

用法：
    python inline_manifest.py

注意：换题库 / 重跑 gen_audio.py 之后，**必须重新执行本脚本**，
否则内联的还是上一版 manifest（表现：新句子没声音，回退成合成音）。
"""
import io
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(ROOT, "index.html")
MANIFEST = os.path.join(ROOT, "audio", "manifest.json")
START = "/* MANIFEST_INLINE_START */"
END = "/* MANIFEST_INLINE_END */"


def main():
    if not os.path.exists(MANIFEST):
        raise SystemExit(f"[错误] 找不到 {MANIFEST}，请先跑 gen_audio.py")

    man = json.load(io.open(MANIFEST, encoding="utf-8"))

    # 紧凑输出；ensure_ascii=False 保留原文，便于排查
    payload = "const AUDIO_MANIFEST = " + json.dumps(
        man, ensure_ascii=False, separators=(",", ":")
    ) + ";"

    s = io.open(HTML, encoding="utf-8").read()
    i, j = s.find(START), s.find(END)
    if i < 0 or j < 0:
        raise SystemExit("[错误] index.html 里找不到 MANIFEST_INLINE_START / END 标记")
    if j < i:
        raise SystemExit("[错误] END 标记出现在 START 之前，文件可能已损坏")

    s = s[:i] + START + "\n" + payload + "\n" + s[j:]
    io.open(HTML, "w", encoding="utf-8").write(s)

    print("已内联 manifest：w {} / q {} / s {} / a {} / m {} 条".format(
        len(man["w"]), len(man["q"]), len(man["s"]), len(man["a"]), len(man["m"])
    ))
    print("index.html 现为 {:.0f} KB".format(os.path.getsize(HTML) / 1024))


if __name__ == "__main__":
    main()
