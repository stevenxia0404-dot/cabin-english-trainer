# -*- coding: utf-8 -*-
"""修正第三关问答的角色错位（挪位法）。

背景：q/a 里有一批是「服务方问 → 客人答」，学员练成了客人点单的话。
改法：q 换成客人的需求/提问，原来的服务方问句整句挪到 a。
s（跟读短句）原本都是服务方视角、全部正确，一律不动。

用法：python patch_vocab_roles.py
"""
import io
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "build_vocab.py")

# (行号, 该行必须包含的关键词, 新行内容)
EDITS = [
    # ---- whisky：原服务方问句挪到 a ----
    (41, "whisky", '    "q":"I\'d like a whisky, please.","a":"How would you like your whisky, sir?",'),
    (42, "威士忌", '    "qz":"我要一杯威士忌，谢谢。","az":"您的威士忌要怎么喝，先生？",'),
    (44, "variants", '    "variants":["Can I have a whisky?","Whisky for me, please."],'),
    (46, "samples", '    "samples":["Would you like it on the rocks?","With ice or straight up, sir?"]},'),
    # ---- Earl Grey：a 与 s 重复，改 a；v/m 去掉客人视角 ----
    (71, "Earl Grey", '    "q":"Which black tea do you have?","a":"Yes, we serve Earl Grey and English Breakfast.",'),
    (72, "红茶", '    "qz":"有什么红茶？","az":"有的，我们供应伯爵茶和英式早餐茶。",'),
    (74, "variants", '    "variants":["Do you serve Earl Grey?","What black teas are available?"],'),
    (76, "samples", '    "samples":["We also have English Breakfast.","Earl Grey is our most popular black tea."]},'),
    # ---- black coffee ----
    (89, "coffee", '    "q":"Do you have black coffee?","a":"Yes, we serve black coffee, sir.",'),
    (90, "咖啡", '    "qz":"有黑咖啡吗？","az":"有的，我们供应黑咖啡，先生。",'),
    (92, "variants", '    "variants":["Is black coffee available?","Can I get a black coffee?"],'),
    (94, "samples", '    "samples":["Black coffee is available, sir.","We can prepare black coffee for you."]},'),
    # ---- latte：只换掉客人视角的第二条例句 ----
    (112, "samples", '    "samples":["We serve latte and brewed coffee.","Latte is our most popular coffee."]},'),
    # ---- Oolong tea ----
    (116, "Oolong", '    "q":"What tea do you have today?","a":"Would you like your usual Oolong tea, sir?",'),
    (117, "茶", '    "qz":"今天有什么茶？","az":"您今天还是喝常喝的乌龙茶吗，先生？",'),
    (119, "variants", '    "variants":["Which teas are available?","Do you have Oolong tea?"],'),
    (121, "samples", '    "samples":["We also serve Pu\'er and Dragon Well.","Oolong tea is ready for you, sir."]},'),
    # ---- rye roll ----
    (269, "rye", '    "q":"Can I have some bread?","a":"Certainly, would you like a rye roll?",'),
    (270, "面包", '    "qz":"能给我些面包吗？","az":"当然，您要黑麦面包吗？",'),
    (272, "variants", '    "variants":["Could I get some bread?","Do you have any bread?"],'),
    (274, "samples", '    "samples":["We have rye roll and sesame bread.","May I suggest the rye roll, sir?"]},'),
    # ---- dressing ----
    (287, "dressing", '    "q":"I\'d like the salad, please.","a":"Thousand island or Italian dressing, sir?",'),
    (288, "色拉", '    "qz":"我要一份色拉，谢谢。","az":"千岛酱还是意式酱，先生？",'),
    (290, "variants", '    "variants":["Can I have a salad?","I\'ll take the salad."],'),
    (292, "samples", '    "samples":["We have French and Italian dressing.","May I suggest the thousand island?"]},'),
    # ---- vanilla：samples 原与 a 完全重复，一并换掉 ----
    (308, "anilla",'    "q":"What ice cream do you have?","a":"We have vanilla and strawberry, sir.",'),
    (309, "口味", '    "qz":"有什么冰淇淋？","az":"有香草和草莓，先生。",'),
    (311, "variants", '    "variants":["Which ice cream flavors are there?","Is vanilla available?"],'),
    (313, "samples", '    "samples":["Vanilla and chocolate are available.","May I suggest the vanilla, sir?"]},'),
    # ---- chocolate ----
    (326, "chocolate", '    "q":"Do you have any chocolate?","a":"Yes, would you care for some chocolate?",'),
    (327, "巧克力", '    "qz":"有巧克力吗？","az":"有的，您要来点巧克力吗？",'),
    (329, "variants", '    "variants":["Is chocolate available?","Can I have some chocolate?"],'),
    (331, "samples", '    "samples":["We have chocolate after the meal.","Chocolate is available, sir."]},'),
    # ---- cashew：只换掉客人视角的第二条例句 ----
    (340, "samples", '    "samples":["We serve cashews and almonds.","The cashews are freshly roasted."]},'),
    # ---- almond ----
    (344, "lmond", '    "q":"Can I have some nuts?","a":"Would you prefer almonds or cashews, sir?",'),
    (345, "坚果", '    "qz":"能给我点坚果吗？","az":"您想要杏仁还是腰果，先生？",'),
    (347, "variants", '    "variants":["Could I get some nuts?","What nuts do you have?"],'),
    (349, "samples", '    "samples":["We have almonds and cashews today.","May I suggest the roasted almonds?"]},'),
    # ---- lavatory：例句与跟读句重复，换掉 ----
    (397, "samples", '    "samples":["It\'s at the front of the cabin.","It\'s just ahead on your left."]},'),
    # ---- Could you repeat that：原 q/v 与 a 语义撞车，改为客人含糊表达 ----
    (422, "repeat", '    "q":"I\'d like the, um, the beef I think.","a":"Could you repeat that, please?",'),
    (423, "重复", '    "qz":"我要那个，嗯，牛肉吧。","az":"能请您重复一遍吗？",'),
    (425, "variants", '    "variants":["The chicken, no wait, the fish.","Can I get, you know, that one?"],'),
]


def main():
    lines = io.open(SRC, encoding="utf-8").read().splitlines(keepends=True)
    shutil.copyfile(SRC, SRC + ".bak-roles")
    print("已备份 -> build_vocab.py.bak-roles")

    ok = 0
    for lineno, keyword, newline in EDITS:
        idx = lineno - 1
        if not (0 <= idx < len(lines)):
            raise SystemExit("行号越界: %d" % lineno)
        old = lines[idx]
        if keyword not in old:
            raise SystemExit(
                "第 %d 行未含关键词 %r，可能行号变了，已中止。\n实际内容: %s"
                % (lineno, keyword, old.rstrip())
            )
        lines[idx] = newline + "\n"
        ok += 1

    io.open(SRC, "w", encoding="utf-8").write("".join(lines))
    print("已替换 %d 行（共 %d 处）" % (ok, len(EDITS)))


if __name__ == "__main__":
    main()
