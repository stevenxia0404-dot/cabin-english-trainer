# -*- coding: utf-8 -*-
"""同步部署目录：只把 manifest 真正引用到的 mp3 复制进 _app/audio。

为什么需要这一步：
换题库后，本地 audio/ 会残留旧句子生成的孤儿 mp3。这些孤儿在沙箱环境里
用 os.remove 常常删不掉（回收站不可用会抛 OSError，见 gen_audio.py --clean 的容错处理）。
部署包只装 manifest 引用到的文件，既保持干净，又绕开了删除限制。

用法：
    python sync_app.py
"""
import io
import json
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(ROOT, "audio")
MANIFEST = os.path.join(AUDIO, "manifest.json")
APP = os.path.join(ROOT, "_app")


def main():
    if not os.path.exists(MANIFEST):
        raise SystemExit("找不到 %s，请先跑 gen_audio.py" % MANIFEST)

    man = json.load(io.open(MANIFEST, encoding="utf-8"))

    # manifest 结构：w/q/m 存文件名字符串；s/a 存 {n, s} 对象
    need = set()
    for kind in ("w", "q", "m"):
        need.update(man[kind].values())
    for kind in ("s", "a"):
        for e in man[kind].values():
            need.add(e["n"])
            need.add(e["s"])

    missing = [f for f in need if not os.path.exists(os.path.join(AUDIO, f))]
    if missing:
        raise SystemExit("以下音频缺失，请先跑 gen_audio.py：%s" % missing[:5])

    # 重建 _app（manifest 已内联进 index.html，故不再单独复制 manifest.json）
    # 受限环境（沙箱 / 回收站不可用）下 rmtree 会抛错，此时退化为覆盖同步：
    # 旧孤儿 mp3 会残留，但部署包功能不受影响，只是体积略大。
    if os.path.exists(APP):
        try:
            shutil.rmtree(APP, ignore_errors=True)
        except Exception as e:
            print("    注意：_app 清理失败，改为覆盖同步（%s）" % e)
    os.makedirs(os.path.join(APP, "audio"), exist_ok=True)

    for name in ("index.html", "data.js"):
        shutil.copyfile(os.path.join(ROOT, name), os.path.join(APP, name))
    for f in need:
        shutil.copyfile(os.path.join(AUDIO, f), os.path.join(APP, "audio", f))

    total = sum(os.path.getsize(os.path.join(APP, "audio", f))
                for f in os.listdir(os.path.join(APP, "audio")) if f.endswith(".mp3"))
    local = len([f for f in os.listdir(AUDIO) if f.endswith(".mp3")])

    print("已同步 %d 个 mp3 -> _app/audio（音频 %.1f MB）" % (len(need), total / 1024 / 1024))
    print("本地 audio/ 共 %d 个 mp3，其中 %d 个是孤儿（未复制进部署包）"
          % (local, local - len(need)))
    print("manifest 已内联在 index.html 中，故部署包不再单独含 manifest.json")


if __name__ == "__main__":
    main()
