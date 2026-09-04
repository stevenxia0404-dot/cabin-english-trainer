# -*- coding: utf-8 -*-
# 把 5 份真实培训资料结构化，生成：
#   1) data.js.draft  —— 可直接替换 index.html 所用的占位 data.js
#   2) 清洗结果_审核版.html —— 供 Steven 逐条审核的整理文档
import json, os, html

BASE = r"C:\Users\86139\Desktop\steven\公务英语AI陪练"

# ====================== 结构化数据（全部源自 5 份资料）======================
# q  = 考官问题(英文，考官扮演外国旅客的提问/场景)
# a  = 标准应答(英文，学员/乘务员应答)
# qz/az = 中译； key/keyz = 信号词； variants = 考官其它问法；
# accept = 关键信息槽（自查/判分用）； samples = 同义说法（第三关溯源用）

scenes = [
 {
  "id": "boarding", "icon": "✈️", "name": "登机与迎宾",
  "desc": "登机口到入座期间的高频问答（查票、引导、挂衣、热毛巾、迎宾饮料、设备）",
  "pairs": [
   {"q":"Excuse me, could you show me to my seat?","a":"Sure. Your seat number is 8A, in the business class. Please follow me.",
    "qz":"打扰一下，能带我到座位吗？","az":"当然，您的座位是 8A，在公务舱，请跟我来。",
    "key":"seat / follow me","keyz":"座位 / 跟我来",
    "variants":["Where is my seat, please?","Could you help me find my seat?"],
    "accept":[["8a","8 a","seat number"],["follow me","this way","business class"]],
    "samples":["Your seat is 8A — please follow me.","Sure, your seat is 8A in business class, this way please."]},

   {"q":"Could you help me with my overcoat?","a":"Of course, sir. I'll hang it up for you. Your clothing will be kept properly.",
    "qz":"能帮我挂一下大衣吗？","az":"当然先生，我帮您挂起来，衣物会妥善保管。",
    "key":"hang up / overcoat","keyz":"挂起 / 大衣",
    "variants":["Would you like me to hang up your coat?","May I help you with your luggage?"],
    "accept":[["hang up","hang","hanging"],["kept properly","keep","properly"]],
    "samples":["Sure, I'll hang your overcoat for you.","Of course, let me hang it up and keep it safe."]},

   {"q":"May I have a hot towel, please?","a":"Here is the hot towel for you. Later we will be serving you welcome drinks.",
    "qz":"能给我热毛巾吗？","az":"这是给您的热毛巾。稍后我们还会提供迎宾饮料。",
    "key":"hot towel","keyz":"热毛巾",
    "variants":["Could I get a hot towel?","Here is the hot towel for you."],
    "accept":[["hot towel","towel"]],
    "samples":["Here you are, a hot towel for you.","Sure, here is your hot towel."]},

   {"q":"What welcome drinks do you have?","a":"We have orange juice, mineral water, champagne and our special 'Young'. Which one would you like?",
    "qz":"你们有什么迎宾饮料？","az":"我们有橙汁、矿泉水、香槟和特饮“青春飞扬”，您喜欢哪一种？",
    "key":"welcome drinks / which one","keyz":"迎宾饮料 / 哪一种",
    "variants":["What would you like to drink?","We have orange juice and water, which do you prefer?"],
    "accept":[["orange juice"],["water","mineral water"],["champagne"],["young"]],
    "samples":["For welcome drinks we have orange juice, water, champagne and Young.","We offer orange juice, water, champagne and our special Young — which would you like?"]},

   {"q":"Where can I charge my electronic device?","a":"You can charge your devices by this USB port, or the socket underneath your armrest.",
    "qz":"我在哪里可以给电子设备充电？","az":"您可以用这个 USB 接口，或者扶手下方的插座充电。",
    "key":"charge / USB port","keyz":"充电 / USB 接口",
    "variants":["Where is the charging port?","How do I charge my phone?"],
    "accept":[["usb port","usb"],["socket","armrest","underneath"]],
    "samples":["You may use this USB port or the socket under your armrest.","Charge via the USB port or the outlet below your armrest."]},
  ]
 },
 {
  "id": "meal", "icon": "🍽️", "name": "餐饮服务",
  "desc": "订餐、主菜/面包/芝士/甜品介绍，以及餐食受损的 ASSAM 处置",
  "pairs": [
   {"q":"Could you tell me what you have for the main course today?","a":"For entree today we have four choices: pan-fried duck breast with rice; stir-fried prawn and abalone with udon noodles in hot bean sauce; pan-fried AUS beef steak with pumpkin duchesse in red wine sauce; and pan-fried lobster with crushed truffle potato in lobster sauce. Which one would you like to have?",
    "qz":"能告诉我今天主菜有哪些吗？","az":"今天主菜有四选一：煎蜜糖鸭胸配饭；鲍鱼虾仁乌冬面配干烧汁；红酒汁煎澳洲牛眼肉配南瓜土豆花；煎龙虾配黑菌土豆泥。您需要哪一种？",
    "key":"main course / four choices","keyz":"主菜 / 四选一",
    "variants":["What are the entree choices today?","May I take your order?"],
    "accept":[["duck breast"],["prawn abalone","abalone"],["beef steak"],["lobster"]],
    "samples":["Today we have four main courses — duck breast, prawn abalone udon, beef steak, and lobster.","For entree we offer four choices; which would you prefer?"]},

   {"q":"What kind of bread do you have?","a":"We have soft roll, hard roll, rye roll, garlic slices and sesame bread. Which one would you like?",
    "qz":"你们有什么面包？","az":"我们有软包、硬包、黑麦面包、蒜蓉面包和芝麻面包，您喜欢哪种？",
    "key":"bread / which one","keyz":"面包 / 哪一种",
    "variants":["Would you like some bread?","Do you have any bread?"],
    "accept":[["soft roll"],["hard roll"],["rye roll"],["garlic slices"],["sesame bread"]],
    "samples":["We offer soft, hard, rye, garlic and sesame bread.","We have soft roll, hard roll, rye, garlic slices and sesame bread."]},

   {"q":"Which cheese would you recommend?","a":"For hard cheese we have British Cheddar, Double Gloucester, Swiss Gruyere and Dutch Edam; for soft cheese French Brie; for crumbly cheese Danish Blue. Which one would you like?",
    "qz":"您推荐哪种芝士？","az":"硬身芝士有英国车达、格罗斯特、瑞士古老也、荷兰红波；软身有法式必然；松碎有丹麦蓝。您喜欢哪种？",
    "key":"cheese / recommend","keyz":"芝士 / 推荐",
    "variants":["What cheese do you have?","Which cheese would you like?"],
    "accept":[["cheddar"],["gruyere"],["edam"],["brie"],["danish blue"]],
    "samples":["We have Cheddar, Gruyere, Edam, Brie and Danish Blue.","For cheese we offer hard, soft and crumbly varieties — which do you prefer?"]},

   {"q":"What do you have for dessert?","a":"For dessert we have coconut cake or ice cream. Which flavor would you like for the ice cream?",
    "qz":"甜品有什么？","az":"甜品有椰子蛋糕或冰淇淋，冰淇淋您喜欢什么口味？",
    "key":"dessert / ice cream","keyz":"甜品 / 冰淇淋",
    "variants":["Any dessert today?","Which dessert would you like?"],
    "accept":[["coconut cake"],["ice cream"]],
    "samples":["We have coconut cake or ice cream for dessert.","Dessert is coconut cake or ice cream — which flavor?"]},

   {"q":"Excuse me, the meal is cold. / The meal is a little spicy and I can't eat spicy food.","a":"I am terribly sorry that you didn't enjoy your meal. If I were you, I would also feel upset. Would you like to try another choice? We still have pan-fried lobster with crushed truffle potato and stir-fried prawn with abalone. May I offer you a glass of champagne as our sincere apology? Thank you for your understanding, and we will try our best to improve our service.",
    "qz":"抱歉，餐食凉了/太辣了我吃不了辣。","az":"非常抱歉您没吃好。若我是您也会不舒服。要不要换一个？我们还有煎龙虾配松露土豆和鲍鱼虾仁。能否敬您一杯香槟致歉？感谢理解，我们会尽力改进。",
    "key":"meal / ASSAM","keyz":"餐食 / ASSAM 程序",
    "variants":["The food is not to my taste.","I didn't enjoy this meal."],
    "accept":[["sorry","apologize","terribly sorry"],["understand","upset","empathy"],["another choice","try again"],["champagne","apology"],["improve","better"]],
    "samples":["I'm so sorry you didn't enjoy it. May I offer another choice and a glass of champagne?","I really apologize — let me bring you another dish right away."]},
  ]
 },
 {
  "id": "beverage", "icon": "🍷", "name": "酒水饮料",
  "desc": "红白葡萄酒推荐（品牌/产地/年份/特点）、特饮鸡尾酒、威士忌喝法",
  "pairs": [
   {"q":"Could you recommend a red wine to go with my beef steak?","a":"Would you like the red wine with strong tannin? We recommend De Bortoli Family Selection Shiraz Cabernet from Australia, 2024 vintage — a full-bodied red with rather strong tannin, a perfect partner for your beef steak. Which one do you prefer?",
    "qz":"能推荐一款配牛排的红葡萄酒吗？","az":"您要单宁较重的吗？推荐澳大利亚 2024 年份德保利家族精选设拉子赤霞珠，酒体饱满、单宁丰富，是牛排的绝佳搭配。您喜欢哪一款？",
    "key":"red wine / beef steak","keyz":"红葡萄酒 / 牛排",
    "variants":["What red wine goes with steak?","Recommend a red wine for my beef, please."],
    "accept":[["de bortoli","deportoli"],["shiraz cabernet"],["australia"],["2024"],["strong tannin","tannin"]],
    "samples":["I'd suggest the De Bortoli Shiraz Cabernet, 2024, full-bodied with strong tannin.","For your steak, the Australian De Bortoli Shiraz Cabernet 2024 pairs perfectly."]},

   {"q":"I'd like some white wine to go with my seafood.","a":"I would recommend our Mapu Sauvignon Blanc from Chile, 2025 vintage — it has a mild body with fresh fruit flavor, which goes well with your seafood.",
    "qz":"我想来点白葡萄酒配海鲜。","az":"推荐智利 2025 年份大地长相思白葡萄酒，酒体适中、果味清新，很搭您的海鲜。",
    "key":"white wine / seafood","keyz":"白葡萄酒 / 海鲜",
    "variants":["Which white wine for my seafood?","A white wine to match the fish, please."],
    "accept":[["mapu"],["sauvignon blanc"],["chile","chile"],["2025"],["seafood"]],
    "samples":["May I suggest the Chilean Mapu Sauvignon Blanc 2025 for your seafood?","The Mapu Sauvignon Blanc from Chile 2025 pairs nicely with seafood."]},

   {"q":"Could you recommend one of your special drinks or cocktails?","a":"May I recommend our special drink 'Bright Future'? It is orange juice mixed with lemon juice and tonic water, with a little salt — refreshing, fruity and well balanced. We also have Mimosa, Gin Tonic and Cuba Libre. Which one would you prefer?",
    "qz":"能推荐一款特饮或鸡尾酒吗？","az":"推荐特饮“明亮前橙”：橙汁加柠檬汁、汤力水与少许盐，清爽果香平衡。我们还有含羞草、金汤力、自由古巴。您喜欢哪种？",
    "key":"special drink / cocktail","keyz":"特饮 / 鸡尾酒",
    "variants":["What cocktails do you have?","Any signature drink?"],
    "accept":[["bright future"],["orange juice"],["lemon"],["tonic water"],["salt"]],
    "samples":["Try our Bright Future — orange juice, lemon, tonic water and a touch of salt.","I'd recommend Bright Future, or a Mimosa / Gin Tonic if you prefer."]},

   {"q":"How would you like your whisky?","a":"On the rocks, with a chaser, or straight up — which do you prefer?",
    "qz":"您的威士忌怎么喝？","az":"加冰、追水还是直饮，您喜欢哪种？",
    "key":"whisky / how","keyz":"威士忌 / 怎么喝",
    "variants":["Whiskey with ice or straight?","How do you serve the whisky?"],
    "accept":[["on the rocks","rocks","ice"],["chaser"],["straight","straight up"]],
    "samples":["On the rocks, as a chaser, or straight — your choice.","With ice, with a chaser, or neat?"]},
  ]
 },
 {
  "id": "response", "icon": "💬", "name": "应答与祝福",
  "desc": "面对旅客表扬、意见建议，以及生日/蜜月/纪念日等祝福场景的标准回应",
  "pairs": [
   {"q":"Thank you so much. The meal was delicious, and your service was wonderful. This is the best flight I've ever had!","a":"Thank you very much for your compliment. It's my great pleasure to serve you, and I'm so glad you enjoyed the meal and our service. I will share your kind words with our whole crew. We give you our best wishes and hope to fly with you again!",
    "qz":"太感谢了，餐食美味、服务周到，这是我坐过最好的航班！","az":"非常感谢您的称赞，能为您服务是我的荣幸。我会把您的夸奖分享给全体机组。送上最衷心祝福，希望再与您同机。",
    "key":"compliment / thank you","keyz":"表扬 / 感谢",
    "variants":["You've done a great job, thank you.","Wonderful service, I appreciate it."],
    "accept":[["thank you","compliment"],["pleasure","glad"],["share","crew"],["hope to fly","again"]],
    "samples":["Thank you for the kind words — it's my pleasure to serve you.","I'm so glad you enjoyed it; I'll pass your praise to the crew."]},

   {"q":"May I make a suggestion? I think the choice of English magazines on board could be wider. You don't need to reply to me — I just want to let you know.","a":"Thank you very much for your feedback and suggestions. It is really an honor to have a passenger like you. I will pass your suggestion on to our company, and we will try our best to improve our service as soon as possible.",
    "qz":"我能提个建议吗？机上英文杂志种类可再丰富些，不必回复我，只是想说一声。","az":"非常感谢您的反馈与建议，有您这样的旅客是我们的荣幸。我会把建议转达公司，并尽快改进服务。",
    "key":"suggestion / feedback","keyz":"建议 / 反馈",
    "variants":["I have a small suggestion about the service.","Just wanted to share some feedback."],
    "accept":[["thank you","feedback"],["pass","company"],["improve","better"]],
    "samples":["Thank you for the suggestion — I'll pass it to our company.","I appreciate your feedback and will share it with the team."]},

   {"q":"Actually, today is my birthday. I can't believe I'm spending it on a plane!","a":"Happy Birthday to you! We are very glad to have you on this flight on your special day. Here is the greeting card and the birthday cake / a glass of red wine we prepared for you. We give you our best wishes. I hope it can leave you a beautiful memory.",
    "qz":"今天其实是我生日，没想到在飞机上过！","az":"生日快乐！很高兴您特殊的一天选乘我们航班。这是心意卡和为您准备的生日蛋糕/红酒。送上祝福，愿留下美好回忆。",
    "key":"birthday / Happy Birthday","keyz":"生日 / 生日快乐",
    "variants":["It's my birthday today!","Today happens to be my birthday."],
    "accept":[["happy birthday"],["greeting card"],["cake","red wine"],["best wishes","memory"]],
    "samples":["Happy Birthday! Here is a greeting card and a birthday cake for you.","Many happy returns — we've prepared a card and a cake for you."]},

   {"q":"My wife and I are on our honeymoon trip to China — we both love Chinese culture!","a":"Congratulations on your wedding! You two are a perfect match. We are very glad to have you on this flight today. Here is a greeting card and two glasses of red wine for you. We give you our best wishes — congratulations and best wishes to you both!",
    "qz":"我和妻子来中国度蜜月，我们都热爱中国文化！","az":"祝贺新婚！你们真是天造地设的一对。很高兴您选乘本次航班。这是心意卡和两杯红酒。送上最衷心祝贺与祝福！",
    "key":"honeymoon / congratulations","keyz":"蜜月 / 祝贺",
    "variants":["We're celebrating our wedding anniversary.","We're here for our son's graduation."],
    "accept":[["congratulations","congrat"],["perfect match"],["greeting card"],["red wine"],["best wishes"]],
    "samples":["Congratulations on your wedding — here's a card and two glasses of red wine!","Happy honeymoon! We've prepared a greeting card and wine for you both."]},
  ]
 },
 {
  "id": "special", "icon": "⚠️", "name": "特殊场景·ASSAM",
  "desc": "按 ASSAM 程序处置：致歉→共情→补救→感谢理解→维护关系（含系统/卫生/秩序/健康等）",
  "pairs": [
   {"q":"Miss, can I have a glass of B52, please?","a":"I am sorry that the cocktail you mentioned is not available on this flight. Would you like to change your order? May I recommend some of our cocktails? We have the Black Russian, the Gin Tonic, and the Mimosa — champagne with orange juice. We also have our special 'Bright Future'. Which one would you prefer?",
    "qz":"小姐，能给我一杯 B52 吗？","az":"很抱歉该鸡尾酒本航班未提供。要不要换一杯？推荐黑俄罗斯、金汤力、含羞草，还有特饮“明亮前橙”。您喜欢哪种？",
    "key":"B52 / not available","keyz":"B52 / 没有供应",
    "variants":["Do you have a B52?","I'd like a B52, please."],
    "accept":[["sorry","apologize","not available"],["understand","looking forward"],["change","recommend"],["thank you"],["enjoy","improve"]],
    "samples":["I'm sorry, B52 isn't on board — may I suggest a Mimosa or our Bright Future?","That cocktail isn't available; let me recommend another for you."]},

   {"q":"My earring just slipped into the seat gap and I can't reach it at all.","a":"I'm so sorry to hear that. Please don't worry — we will help you. For your safety, please do not adjust the business-class seat by yourself. After landing, I will contact the mechanic personnel to help you.",
    "qz":"我的耳环掉进座椅缝隙，完全够不着。","az":"很抱歉听到这事，别担心我们会帮忙。为安全请勿自行调节公务舱座椅，落地后我联系机务协助取出。",
    "key":"earring / seat gap","keyz":"耳环 / 座椅缝",
    "variants":["Something fell into the seat crack.","I dropped my earring in the seat."],
    "accept":[["sorry","don't worry"],["do not adjust","safety"],["after landing","mechanic"],["thank you","cooperation"]],
    "samples":["Don't worry — after landing I'll ask our mechanic to retrieve it.","Please don't move the seat; we'll have engineering help after landing."]},

   {"q":"The passenger in front of me is playing videos. I'm trying to get some sleep.","a":"I am so sorry that this has disturbed your rest. If I were you, I would also feel uncomfortable. Let me communicate with the passenger in front of you right away, and I will politely ask him to use his earphones. May I also offer you a pair of earplugs and a blanket so you can rest better?",
    "qz":"前排旅客在放视频，我想睡觉。","az":"很抱歉打扰了您休息。若我是您也会不适。我马上与前排沟通，请他用耳机。需要耳塞和毛毯帮您更好休息吗？",
    "key":"videos / rest","keyz":"视频 / 休息",
    "variants":["The person ahead is watching videos loudly.","I can't sleep with the noise."],
    "accept":[["sorry","disturbed"],["understand","uncomfortable"],["earphones","communicate"],["earplugs","blanket"],["thank you"]],
    "samples":["I'm sorry for the disturbance — let me ask him to use earphones.","So sorry; I'll speak to the passenger ahead and offer you earplugs."]},

   {"q":"Miss, I've got a headache. Maybe I've caught a cold. And I feel a little airsick.","a":"I'm sorry to hear that. I totally understand how you feel. I have prepared some tissues for you. How about having a cup of warm lemon water? May I recline your seat? Please take a good rest. If you feel airsick, I will bring you an airsickness bag right away.",
    "qz":"小姐，我头痛可能感冒了，还有点晕机。","az":"很遗憾听到您不适，完全理解。已备纸巾，来杯温柠檬水好吗？帮您放平座椅好好休息，若晕机立刻拿来呕吐袋。",
    "key":"headache / airsick","keyz":"头痛 / 晕机",
    "variants":["I feel sick and have a headache.","I think I'm coming down with something."],
    "accept":[["sorry","understand"],["tissues"],["warm lemon water"],["recline","rest"],["airsickness bag"]],
    "samples":["I'm sorry you feel unwell — let me get tissues and warm lemon water.","So sorry; may I recline your seat and bring a warm drink?"]},

   {"q":"Miss, my entertainment system has collapsed... / My seat cannot lie flat.","a":"I am so sorry about that. I will reset your entertainment system right away. It will take about 10 minutes. Please avoid using the remote control for the time being, and I will be back to check your system. Would you like some newspapers or magazines during this period?",
    "qz":"小姐，我的娱乐系统坏了/座椅不能平躺。","az":"很抱歉，我马上重启系统，约十分钟。期间请勿操作遥控器，我会回来确认。这段时间需要报刊杂志吗？",
    "key":"entertainment / reset","keyz":"娱乐系统 / 重启",
    "variants":["My screen is frozen.","The IFE is not working."],
    "accept":[["sorry","apologize"],["reset","10 minutes"],["remote control","avoid"],["newspapers","magazines"],["check","back"]],
    "samples":["I'll reset it now — about 10 minutes; please don't use the remote.","So sorry; let me restart the system and check back shortly."]},

   {"q":"I just came out of the lavatory — the hygiene condition there is really worrying.","a":"I am terribly sorry that the lavatory did not meet our hygiene standards. I will clean and tidy the lavatory right away, and I will check it regularly for the rest of the flight. May I offer you a hot towel?",
    "qz":"我刚从洗手间出来，卫生状况堪忧。","az":"非常抱歉洗手间未达标准，我立刻清洁整理，并在航程中持续检查，需要热毛巾吗？",
    "key":"lavatory / hygiene","keyz":"洗手间 / 卫生",
    "variants":["The restroom is not clean.","The toilet is in a bad state."],
    "accept":[["sorry","hygiene"],["clean","tidy","right away"],["check regularly"],["hot towel"],["thank you"]],
    "samples":["I'm terribly sorry — I'll clean it now and keep checking.","So sorry about that; let me tidy the lavatory immediately."]},

   {"q":"The ground staff promised our family would sit together, but our boarding passes show separate seats! My daughter is only five.","a":"I am so sorry that your seats were separated. Please don't worry. Let me check the seats right away and communicate with passengers nearby to arrange seats together for your family. I will also report this to the ground staff so we can improve our service.",
    "qz":"地勤说我们一家人坐一起，可登机牌是分开的，女儿才五岁！","az":"很抱歉座位被分开了。别急，我立刻查座并协调邻座帮您全家坐一起，也会向地勤反馈改进。",
    "key":"family / separate seats","keyz":"家人 / 分开座位",
    "variants":["We were supposed to sit together.","Our seats are not together."],
    "accept":[["sorry","separated"],["don't worry","check"],["arrange","together"],["report","ground staff"],["improve"]],
    "samples":["I'm sorry — let me rearrange seats for your family right away.","So sorry; I'll coordinate with nearby passengers to seat you together."]},
  ]
 },
]

# ====================== 词汇表（源自 PPTX 酒水/餐食词汇）======================
vocab = [
 {"cat":"红葡萄酒 Red Wine","items":[["Great Wall Five-Star G7","长城五星G7干红"],["Terrazas 1001 Classic Malbec","台阶安第斯1001马尔贝克"],["De Bortoli Shiraz Cabernet","德保利设拉子赤霞珠"],["Chateau Passe Craby","高碧城堡超级波尔多"],["Barrel Estate New World Shiraz","宝珞新世界西拉"],["Penfolds Koonunga Hill Shiraz Cabernet","奔富蔻兰山设拉子赤霞珠"],["Girard Napa Zinfandel","纳帕谷杰拉德仙芬黛"],["P. Ferraud & Fils","皮·费罗父子赤霞珠"],["Gerard Bertrand 6Eme Sens","吉哈伯通第六感"]]},
 {"cat":"白葡萄酒 White Wine","items":[["Mapu Sauvignon Blanc","大地长相思白"],["Barrel Estate Chardonnay","宝珞霞多丽"],["Mouton Cadet White","木桐嘉棣白"],["Windsor Chardonnay","温莎霞多丽"],["Frontera Sauvignon Blanc","缘峰长相思"]]},
 {"cat":"香槟/气泡 Champagne","items":[["Champagne Gremillet Ambassadeur","甘露天泉大使香槟"],["Champagne Robert de Pampignac","罗伯特潘皮尼亚香槟"],["Irroy Champagne","艾洛伊金丝带香槟"],["Maxim's Champagne","马克西姆珍藏香槟"]]},
 {"cat":"烈酒/利口酒 Liquors","items":[["Johnnie Walker Black Label","尊尼获加黑牌"],["Remy Martin","人头马干邑"],["Eristoff Vodka","皇太子伏特加"],["Gordon's Gin","哥顿金酒"],["Captain Morgan Rum","摩根船长白朗姆"],["Baileys","百利甜酒"],["GET 27 Peppermint","葫芦绿薄荷酒"],["BARDINET Coffee Liqueur","必得利咖啡力娇酒"]]},
 {"cat":"混合饮料 Mix Drinks","items":[["Gin Tonic","金汤力"],["Mimosa","含羞草"],["Cuba Libre","自由古巴"],["Black Russian","黑俄罗斯"],["Absolut Ginger Ale","绝对干姜"]]},
 {"cat":"茶 Tea","items":[["Longjing / Dragon Well","龙井"],["Tieh-Kwan-Yin","铁观音"],["Pu'er","普洱"],["English Breakfast","英式早餐茶"],["Earl Grey","伯爵茶"],["Oolong","乌龙茶"]]},
 {"cat":"咖啡 Coffee","items":[["Black Coffee","黑咖啡"],["Decaffeinated","低因咖啡"],["Drip Coffee","挂耳咖啡"],["Brewed Coffee","现煮咖啡"],["Latte","拿铁"],["Equal sweetener","怡口糖"]]},
 {"cat":"芝士 Cheese","items":[["British Cheddar","英国车达(硬)"],["Double Gloucester","格罗斯特(硬)"],["Swiss Gruyere","瑞士古老也(硬)"],["Dutch Edam","荷兰红波(硬)"],["French Brie","法式必然(软)"],["Danish Blue","丹麦蓝(松碎)"]]},
 {"cat":"面包 Bread","items":[["Soft roll","软包"],["Hard roll","硬包"],["Rye roll","黑麦面包"],["Garlic slices","蒜蓉面包"],["Sesame bread","芝麻面包"]]},
 {"cat":"肉类 Meat","items":[["Sirloin","西冷牛排"],["Rib eye","牛眼肉牛排"],["Fillet","菲力牛排"],["T-bone","T骨牛排"],["Lamb rack","羊脊排"],["Pork chop","猪排"],["Bacon","培根"],["Sausage","香肠"]]},
 {"cat":"烹饪方式 Cooking","items":[["Pan-fry","盘煎"],["Stir-fry","翻炒"],["Grill","烤"],["Steam","蒸"],["Deep-fry","炸"],["Roast","烘烤"],["Smoke","烟熏"],["Boil","煮"]]},
 {"cat":"甜品/冰淇淋 Dessert","items":[["Coconut cake","椰子蛋糕"],["Chocolate mousse cake","巧克力慕斯"],["Cheese cake","芝士蛋糕"],["Matcha cake","抹茶蛋糕"],["Vanilla / Sea-salted / Blueberry / Oreo","香草/海盐/蓝莓/奥利奥"]]},
 {"cat":"坚果 Nuts","items":[["Almond","杏仁"],["Cashew","腰果"],["Walnut","核桃"],["Pistachio","开心果"],["Macadamia","夏威夷果"],["Hazelnut","榛仁"],["Pecan","山核桃"],["Pine","松子"]]},
]

# ====================== ASSAM 程序速查 ======================
assam = [
 ("A","Apologize 致歉","I'm sorry that... / I really do apologize for... / I am terribly sorry that..."),
 ("S","Show Empathy 共情","If I were you, I would also feel uncomfortable. / I totally understand how you feel."),
 ("S","Solution 补救","May I offer you...? / I will check to see what else we can offer you."),
 ("A","Appreciation 感谢理解","Thank you for your understanding. / Thank you for your feedback and suggestions."),
 ("M","Maintain 维护关系","We will try our best to improve our service. / Hope to fly with you again."),
]

# ====================== 1) 写 data.js.draft ======================
data_obj = {"scenes": scenes}
js = "// 公务舱英语陪练 · 由 5 份培训资料结构化生成（DRAFT，待 Steven 审核）\n"
js += "// 来源：前置课件R1-01 / 公务舱英语R3-06 / 话术手册PDF / 参考答案R1-08 / 试卷R1-01\n"
js += "// 替换原 data.js 前请先审核 accept/samples 是否贴合你的考核口径。\n"
js += "const DATA = " + json.dumps(data_obj, ensure_ascii=False, indent=2) + ";\n"
with open(os.path.join(BASE, "data.js.draft"), "w", encoding="utf-8") as f:
    f.write(js)
print("wrote data.js.draft :", len(scenes), "scenes,",
      sum(len(s['pairs']) for s in scenes), "pairs")

# ====================== 2) 写 审核版 HTML ======================
def esc(x): return html.escape(str(x))

scene_blocks = ""
for s in scenes:
    rows = ""
    for i, p in enumerate(s["pairs"], 1):
        rows += f"""
        <tr>
          <td class="idx">{i}</td>
          <td class="en">{esc(p['q'])}</td>
          <td class="en a">{esc(p['a'])}</td>
          <td class="zh">{esc(p['qz'])}<br>{esc(p['az'])}</td>
          <td class="kw">{esc(p['key'])}<br><span class="muted">{esc(p['keyz'])}</span></td>
          <td class="mini">{esc(' / '.join(p['variants']))}</td>
          <td class="mini">{esc(' / '.join(p['accept'][0]))}</td>
          <td class="mini">{esc(' / '.join(p['samples']))}</td>
        </tr>"""
    scene_blocks += f"""
    <section class="scene">
      <h2>{esc(s['icon'])} {esc(s['name'])} <span class="badge">{len(s['pairs'])} 组</span></h2>
      <p class="desc">{esc(s['desc'])}</p>
      <table>
        <thead><tr><th>#</th><th>考官问题 Q</th><th>标准应答 A</th><th>中文</th><th>信号词</th><th>考官其它问法</th><th>关键信息槽(首槽)</th><th>同义说法</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>
    </section>"""

vocab_blocks = ""
for v in vocab:
    cells = "".join(f"<li><b>{esc(e)}</b> {esc(zh)}</li>" for e, zh in v["items"])
    vocab_blocks += f"<div class='vocab'><h4>{esc(v['cat'])}</h4><ul>{cells}</ul></div>"

assam_rows = "".join(f"<tr><td class='step'>{esc(st)}</td><td>{esc(en)}</td><td class='en'>{esc(ph)}</td></tr>" for st, en, ph in assam)

total = sum(len(s['pairs']) for s in scenes)
html_doc = f"""<!doctype html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>公务舱英语陪练 · 资料清洗结果（审核版）</title>
<style>
  :root{{--bg:#fbf7f2;--card:#fffdfb;--line:#ece3d8;--ink:#3a332b;--muted:#9a8f80;
    --red:#c97a6d;--yellow:#d8b25e;--blue:#7d97b8;--green:#88a888;--orange:#cf9b6b;}}
  *{{box-sizing:border-box}}
  body{{margin:0;font-family:-apple-system,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
    background:var(--bg);color:var(--ink);line-height:1.6;}}
  .wrap{{max-width:1180px;margin:0 auto;padding:28px 20px 80px;}}
  header{{background:linear-gradient(120deg,#f3e6d8,#fbf1e6);border:1px solid var(--line);
    border-radius:16px;padding:22px 26px;margin-bottom:22px;}}
  header h1{{margin:0 0 6px;font-size:22px;}}
  header p{{margin:4px 0;color:var(--muted);font-size:13px;}}
  .stats{{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px;}}
  .stat{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:8px 14px;font-size:13px;}}
  .stat b{{font-size:18px;color:var(--orange);}}
  h2{{font-size:18px;margin:30px 0 6px;border-left:4px solid var(--orange);padding-left:10px;}}
  .badge{{font-size:12px;background:var(--yellow);color:#5a4a1f;border-radius:999px;padding:2px 10px;vertical-align:middle;}}
  .desc{{color:var(--muted);font-size:13px;margin:2px 0 12px;}}
  .scene{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:8px 16px 18px;margin-bottom:18px;}}
  table{{width:100%;border-collapse:collapse;font-size:13px;}}
  th,td{{border:1px solid var(--line);padding:8px 9px;vertical-align:top;text-align:left;}}
  th{{background:#f6ede2;font-weight:600;color:#6b5d4c;}}
  td.idx{{color:var(--muted);text-align:center;width:28px;}}
  td.en{{color:#2f3b4a;}}
  td.en.a{{background:#f3f8f3;}}
  td.zh{{color:#6b5d4c;}}
  td.kw{{background:#fdf3ee;}}
  .kw .muted{{color:var(--muted);font-size:12px;}}
  td.mini{{font-size:12px;color:#5a5044;}}
  .muted{{color:var(--muted);}}
  h3{{font-size:15px;margin:26px 0 8px;color:var(--blue);}}
  .vocab-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;}}
  .vocab{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:10px 14px;}}
  .vocab h4{{margin:0 0 8px;font-size:13px;color:var(--green);}}
  .vocab ul{{margin:0;padding-left:16px;font-size:12.5px;}}
  .vocab li{{margin:3px 0;}}
  table.assam td.step{{font-weight:700;color:var(--red);text-align:center;width:40px;}}
  .note{{background:#fff8ef;border:1px dashed var(--orange);border-radius:12px;padding:14px 18px;font-size:13px;color:#6b5d4c;}}
  footer{{margin-top:30px;color:var(--muted);font-size:12px;text-align:center;}}
</style></head><body><div class="wrap">
<header>
  <h1>公务舱英语陪练 · 资料清洗结果（审核版）</h1>
  <p>资料来源：前置课件 R1-01 · 公务舱英语 R3-06 · 沟通话术手册 PDF · 参考答案 R1-08 · 试卷 R1-01</p>
  <p>说明：下方所有 Q/A 均忠实摘自上述资料，已按 App 的 data.js 字段（q/a/qz/az/key/variants/accept/samples）结构化。</p>
  <div class="stats">
    <div class="stat"><b>{len(scenes)}</b> 个场景</div>
    <div class="stat"><b>{total}</b> 组对话</div>
    <div class="stat"><b>{len(vocab)}</b> 类词汇表</div>
    <div class="stat">ASSAM <b>5</b> 步程序</div>
  </div>
</header>

<div class="note">
  <b>审核要点（替换 data.js 前请确认）：</b><br>
  1) <b>accept（关键信息槽）</b>：目前按"学员应答里必须点到的关键信息"填了首槽示例，建议逐条核对是否贴合你的考核口径（尤其特殊场景是否以 ASSAM 五步为判分点）。<br>
  2) <b>samples（同义说法）</b>：我已按资料给了 2 条，可再补你方官方口径。<br>
  3) <b>长应答</b>：特殊场景/ASSAM 的 A 为完整话术，App 第三关"目标句"会整段播放，确认长度是否合适。<br>
  4) 通过审核后，把 <code>data.js.draft</code> 内容覆盖进 <code>data.js</code> 并重新部署即可（无需改代码）。
</div>

<h2>一、结构化对话（可直接进 App 题库）</h2>
{scene_blocks}

<h2>二、餐饮 / 服务词汇表（源自 PPTX 词汇页）</h2>
<div class="vocab-grid">{vocab_blocks}</div>

<h2>三、ASSAM 沟通程序速查（特殊场景判分骨架）</h2>
<table class="assam"><thead><tr><th>步</th><th>含义</th><th>常用句型</th></tr></thead>
<tbody>{assam_rows}</tbody></table>

<h2>四、字段映射说明</h2>
<table><thead><tr><th>App 字段</th><th>本清洗结果来源</th></tr></thead><tbody>
<tr><td><b>q</b></td><td>参考答案 DOCX 的"参考问题 Question"（考官扮演旅客英文）；或 PDF 话术手册旅客侧句子</td></tr>
<tr><td><b>a</b></td><td>参考答案 DOCX 的"参考答案 Answer"（学员标准英文应答）；长话术为 ASSAM 完整版</td></tr>
<tr><td><b>qz / az</b></td><td>资料中的对应中文</td></tr>
<tr><td><b>key / keyz</b></td><td>Question 中的信号词（听到即知在问什么）</td></tr>
<tr><td><b>variants</b></td><td>同一意思的其它考官问法（取自 PPTX/PDF 同类句式）</td></tr>
<tr><td><b>accept</b></td><td>应答须点到的关键信息槽（第一关听辨/第三关自查用）</td></tr>
<tr><td><b>samples</b></td><td>同义地道说法（第三关"类似句型"面板展示，多重溯源）</td></tr>
</tbody></table>

<footer>生成时间 2026-08-31 · 由 WorkBuddy 劳模结构化输出 · DRAFT 待审核</footer>
</div></body></html>"""

with open(os.path.join(BASE, "清洗结果_审核版.html"), "w", encoding="utf-8") as f:
    f.write(html_doc)
print("wrote 清洗结果_审核版.html")
