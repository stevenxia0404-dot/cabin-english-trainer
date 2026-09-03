// 公务舱英语陪练 · 词汇驱动题库（第一版 48 词／8 类）
// 字段：w/wz=单词+中文(第一关听辨)  s/sz=跟读短句(第二关)  q/a/qz/az=情景应答(第三关)
// 规格：q<=12词 a<=15词 s<=12词，目标词必现在 a 与 s 中
// 音色：考官(男 Brian) 念 w 与 q；示范/应答(女 Jenny) 念 s 与 a
const DATA = {
  "scenes": [
    {
      "id": "drink",
      "icon": "🍷",
      "name": "酒水",
      "desc": "红白葡萄酒、香槟、烈酒与鸡尾酒",
      "pairs": [
        {
          "w": "Sauvignon Blanc",
          "wz": "长相思白葡萄酒",
          "s": "This Sauvignon Blanc is from Chile.",
          "sz": "这款长相思白葡萄酒来自智利。",
          "q": "What white wine goes with seafood?",
          "a": "The Mapu Sauvignon Blanc from Chile.",
          "qz": "什么白葡萄酒配海鲜？",
          "az": "智利的 Mapu 长相思白葡萄酒。",
          "key": "Sauvignon Blanc",
          "keyz": "长相思白葡萄酒",
          "variants": [
            "Which white wine do you recommend?",
            "What white wine do you have?"
          ],
          "accept": [
            [
              "sauvignon blanc",
              "sauvignon"
            ],
            [
              "chile",
              "chile"
            ]
          ],
          "samples": [
            "I'd suggest the Chilean Sauvignon Blanc.",
            "The Mapu Sauvignon Blanc pairs well with seafood."
          ]
        },
        {
          "w": "Shiraz Cabernet",
          "wz": "设拉子赤霞珠红葡萄酒",
          "s": "The Shiraz Cabernet has strong tannin.",
          "sz": "这款设拉子赤霞珠单宁丰富。",
          "q": "Which red wine has strong tannin?",
          "a": "The De Bortoli Shiraz Cabernet.",
          "qz": "哪款红酒单宁较重？",
          "az": "德保利设拉子赤霞珠。",
          "key": "Shiraz Cabernet",
          "keyz": "设拉子赤霞珠",
          "variants": [
            "What red wine pairs with steak?",
            "Which red wine is full-bodied?"
          ],
          "accept": [
            [
              "shiraz cabernet",
              "shiraz"
            ]
          ],
          "samples": [
            "I'd recommend the De Bortoli Shiraz Cabernet.",
            "The Shiraz Cabernet from Australia, 2024 vintage."
          ]
        },
        {
          "w": "Champagne",
          "wz": "香槟",
          "s": "Would you like a glass of champagne?",
          "sz": "您要来一杯香槟吗？",
          "q": "What sparkling wine do you have?",
          "a": "We have champagne from France.",
          "qz": "你们有什么气泡酒？",
          "az": "我们有法国香槟。",
          "key": "champagne",
          "keyz": "香槟",
          "variants": [
            "Do you have champagne on board?",
            "What do you have for celebration?"
          ],
          "accept": [
            [
              "champagne"
            ],
            [
              "france",
              "french"
            ]
          ],
          "samples": [
            "We serve French champagne.",
            "Yes, champagne is available on this flight."
          ]
        },
        {
          "w": "whisky",
          "wz": "威士忌",
          "s": "How would you like your whisky?",
          "sz": "您的威士忌怎么喝？",
          "q": "I'd like a whisky, please.",
          "a": "How would you like your whisky, sir?",
          "qz": "我要一杯威士忌，谢谢。",
          "az": "您的威士忌要怎么喝，先生？",
          "key": "whisky",
          "keyz": "威士忌",
          "variants": [
            "Can I have a whisky?",
            "Whisky for me, please."
          ],
          "accept": [
            [
              "on the rocks",
              "rocks",
              "ice"
            ],
            [
              "chaser"
            ],
            [
              "straight",
              "neat"
            ]
          ],
          "samples": [
            "Would you like it on the rocks?",
            "With ice or straight up, sir?"
          ]
        },
        {
          "w": "cocktail",
          "wz": "鸡尾酒",
          "s": "May I recommend a cocktail for you?",
          "sz": "我给您推荐一款鸡尾酒好吗？",
          "q": "Do you have any cocktails?",
          "a": "Yes, we have cocktails, Mimosa and Gin Tonic.",
          "qz": "有鸡尾酒吗？",
          "az": "有，含羞草和金汤力。",
          "key": "cocktail",
          "keyz": "鸡尾酒",
          "variants": [
            "What cocktails are available?",
            "Can I have a cocktail?"
          ],
          "accept": [
            [
              "mimosa"
            ],
            [
              "gin tonic"
            ],
            [
              "cuba libre",
              "black russian"
            ]
          ],
          "samples": [
            "We offer Mimosa, Gin Tonic and Cuba Libre.",
            "Certainly — Mimosa is light and refreshing."
          ]
        },
        {
          "w": "vintage",
          "wz": "（葡萄酒）采摘年份",
          "s": "This red wine is the 2024 vintage.",
          "sz": "这款红酒是 2024 年份。",
          "q": "What vintage is this red wine?",
          "a": "It is the 2024 vintage.",
          "qz": "这款红酒什么年份？",
          "az": "是 2024 年份。",
          "key": "vintage",
          "keyz": "采摘年份",
          "variants": [
            "Which year is this wine from?",
            "How old is this wine?"
          ],
          "accept": [
            [
              "2024",
              "twenty twenty four"
            ]
          ],
          "samples": [
            "This one is a 2024 vintage.",
            "It's from the 2024 harvest."
          ]
        }
      ]
    },
    {
      "id": "hot",
      "icon": "☕",
      "name": "热饮",
      "desc": "中国茶、红茶与各类咖啡",
      "pairs": [
        {
          "w": "Earl Grey",
          "wz": "伯爵茶",
          "s": "We have Earl Grey and English Breakfast.",
          "sz": "我们有伯爵茶和英式早餐茶。",
          "q": "Which black tea do you have?",
          "a": "Yes, we serve Earl Grey and English Breakfast.",
          "qz": "有什么红茶？",
          "az": "有的，我们供应伯爵茶和英式早餐茶。",
          "key": "Earl Grey",
          "keyz": "伯爵茶",
          "variants": [
            "Do you serve Earl Grey?",
            "What black teas are available?"
          ],
          "accept": [
            [
              "earl grey"
            ]
          ],
          "samples": [
            "We also have English Breakfast.",
            "Earl Grey is our most popular black tea."
          ]
        },
        {
          "w": "Pu'er tea",
          "wz": "普洱茶",
          "s": "Our Pu'er tea is very popular.",
          "sz": "我们的普洱茶很受欢迎。",
          "q": "What Chinese tea do you have?",
          "a": "We have Pu'er tea and Dragon Well.",
          "qz": "有什么中国茶？",
          "az": "有普洱和龙井。",
          "key": "Pu'er",
          "keyz": "普洱",
          "variants": [
            "Do you have Pu'er tea?",
            "Which Chinese tea do you recommend?"
          ],
          "accept": [
            [
              "puer",
              "pu'er",
              "pu er"
            ],
            [
              "dragon well",
              "longjing"
            ]
          ],
          "samples": [
            "We serve Pu'er, Tieh-Kwan-Yin and Dragon Well.",
            "Pu'er tea is a good choice."
          ]
        },
        {
          "w": "black coffee",
          "wz": "黑咖啡",
          "s": "Here is your black coffee, sir.",
          "sz": "这是您的黑咖啡，先生。",
          "q": "Do you have black coffee?",
          "a": "Yes, we serve black coffee, sir.",
          "qz": "有黑咖啡吗？",
          "az": "有的，我们供应黑咖啡，先生。",
          "key": "black coffee",
          "keyz": "黑咖啡",
          "variants": [
            "Is black coffee available?",
            "Can I get a black coffee?"
          ],
          "accept": [
            [
              "black coffee",
              "black"
            ],
            [
              "sugar"
            ],
            [
              "milk",
              "cream"
            ]
          ],
          "samples": [
            "Black coffee is available, sir.",
            "We can prepare black coffee for you."
          ]
        },
        {
          "w": "decaffeinated coffee",
          "wz": "低因咖啡",
          "s": "We also have decaffeinated coffee.",
          "sz": "我们也有低因咖啡。",
          "q": "Do you have decaffeinated coffee?",
          "a": "Yes, we have decaffeinated coffee.",
          "qz": "有低因咖啡吗？",
          "az": "有，我们有低因咖啡。",
          "key": "decaffeinated",
          "keyz": "低因/脱咖啡因",
          "variants": [
            "Can I get a decaf?",
            "Is decaf available?"
          ],
          "accept": [
            [
              "decaffeinated",
              "decaf"
            ]
          ],
          "samples": [
            "Certainly, decaf is available.",
            "Yes, we can prepare decaffeinated coffee."
          ]
        },
        {
          "w": "latte",
          "wz": "拿铁",
          "s": "Would you care for a latte?",
          "sz": "您要来杯拿铁吗？",
          "q": "What coffee do you have?",
          "a": "We have latte, drip and black coffee.",
          "qz": "有什么咖啡？",
          "az": "拿铁、挂耳和黑咖啡。",
          "key": "latte",
          "keyz": "拿铁",
          "variants": [
            "Is latte available?",
            "What coffees are on board?"
          ],
          "accept": [
            [
              "latte"
            ],
            [
              "drip coffee",
              "drip"
            ],
            [
              "black coffee"
            ]
          ],
          "samples": [
            "We serve latte and brewed coffee.",
            "Latte is our most popular coffee."
          ]
        },
        {
          "w": "Oolong tea",
          "wz": "乌龙茶",
          "s": "Would you like Oolong tea as usual?",
          "sz": "您今天还是喝乌龙茶吗？",
          "q": "What tea do you have today?",
          "a": "Would you like your usual Oolong tea, sir?",
          "qz": "今天有什么茶？",
          "az": "您今天还是喝常喝的乌龙茶吗，先生？",
          "key": "Oolong",
          "keyz": "乌龙茶",
          "variants": [
            "Which teas are available?",
            "Do you have Oolong tea?"
          ],
          "accept": [
            [
              "oolong"
            ]
          ],
          "samples": [
            "We also serve Pu'er and Dragon Well.",
            "Oolong tea is ready for you, sir."
          ]
        }
      ]
    },
    {
      "id": "dish",
      "icon": "🍽️",
      "name": "菜品",
      "desc": "主菜、汤品、冷荤与早餐",
      "pairs": [
        {
          "w": "duck breast",
          "wz": "鸭胸",
          "s": "The duck breast is pan-fried with rice.",
          "sz": "鸭胸是盘煎配米饭。",
          "q": "What is the first main course?",
          "a": "Pan-fried duck breast with rice.",
          "qz": "第一道主菜是什么？",
          "az": "煎蜜糖鸭胸配米饭。",
          "key": "duck breast",
          "keyz": "鸭胸",
          "variants": [
            "What do you have for the main course?",
            "Tell me about the first choice."
          ],
          "accept": [
            [
              "duck breast",
              "duck"
            ],
            [
              "rice"
            ]
          ],
          "samples": [
            "The first choice is pan-fried duck breast.",
            "We have duck breast served with rice."
          ]
        },
        {
          "w": "beef steak",
          "wz": "牛排",
          "s": "The beef steak comes in red wine sauce.",
          "sz": "牛排配红酒汁。",
          "q": "Which main course do you recommend?",
          "a": "The pan-fried AUS beef steak.",
          "qz": "主菜推荐哪个？",
          "az": "盘煎澳洲牛排。",
          "key": "beef steak",
          "keyz": "牛排",
          "variants": [
            "What is good today?",
            "Recommend a main course, please."
          ],
          "accept": [
            [
              "beef steak",
              "steak"
            ],
            [
              "australia",
              "aus",
              "australian"
            ]
          ],
          "samples": [
            "I'd suggest the Australian beef steak.",
            "The pan-fried beef steak is excellent."
          ]
        },
        {
          "w": "lobster",
          "wz": "龙虾",
          "s": "The lobster comes with truffle potato.",
          "sz": "龙虾配黑菌土豆泥。",
          "q": "What seafood do you have?",
          "a": "We have pan-fried lobster.",
          "qz": "有什么海鲜？",
          "az": "我们有盘煎龙虾。",
          "key": "lobster",
          "keyz": "龙虾",
          "variants": [
            "Any seafood on the menu?",
            "Do you serve lobster?"
          ],
          "accept": [
            [
              "lobster"
            ],
            [
              "truffle potato",
              "truffle"
            ]
          ],
          "samples": [
            "The lobster is served with truffle potato.",
            "We have pan-fried lobster in lobster sauce."
          ]
        },
        {
          "w": "pumpkin cream soup",
          "wz": "奶油南瓜汤",
          "s": "Here is your pumpkin cream soup.",
          "sz": "这是您的奶油南瓜汤。",
          "q": "What soup do you serve?",
          "a": "Pumpkin cream soup, sir.",
          "qz": "汤是什么？",
          "az": "奶油南瓜汤，先生。",
          "key": "pumpkin cream soup",
          "keyz": "奶油南瓜汤",
          "variants": [
            "Which soup is it today?",
            "Any soup to start?"
          ],
          "accept": [
            [
              "pumpkin"
            ],
            [
              "soup",
              "cream soup"
            ]
          ],
          "samples": [
            "We have pumpkin cream soup.",
            "The soup today is pumpkin cream."
          ]
        },
        {
          "w": "congee",
          "wz": "粥",
          "s": "The congee comes with Chinese dim sum.",
          "sz": "粥配中式点心。",
          "q": "What is the Chinese breakfast?",
          "a": "Congee with Chinese dim sum.",
          "qz": "中式早餐是什么？",
          "az": "粥配中式点心。",
          "key": "congee",
          "keyz": "粥",
          "variants": [
            "What do you have for Chinese breakfast?",
            "Is there congee?"
          ],
          "accept": [
            [
              "congee",
              "porridge"
            ],
            [
              "dim sum"
            ]
          ],
          "samples": [
            "We serve congee with pickles and dim sum.",
            "The Chinese breakfast is congee."
          ]
        },
        {
          "w": "omelette",
          "wz": "煎蛋卷／蛋饼",
          "s": "The omelette comes with bacon.",
          "sz": "蛋饼配培根。",
          "q": "What is the Western breakfast?",
          "a": "Omelette with bacon and cereal.",
          "qz": "西式早餐是什么？",
          "az": "蛋饼配培根和麦片。",
          "key": "omelette",
          "keyz": "蛋饼/煎蛋卷",
          "variants": [
            "What do you serve for Western breakfast?",
            "Is there an omelette?"
          ],
          "accept": [
            [
              "omelette",
              "scrambled egg"
            ],
            [
              "bacon",
              "sausage"
            ],
            [
              "cereal"
            ]
          ],
          "samples": [
            "Scrambled egg with bacon and cereal.",
            "We have omelette with sausage."
          ]
        }
      ]
    },
    {
      "id": "cook",
      "icon": "🥩",
      "name": "食材与烹饪",
      "desc": "肉类、海鲜与烹饪方式",
      "pairs": [
        {
          "w": "pan-fried",
          "wz": "盘煎",
          "s": "The steak is pan-fried in red wine sauce.",
          "sz": "牛排是红酒汁盘煎的。",
          "q": "How is the beef cooked?",
          "a": "It is pan-fried, sir.",
          "qz": "牛肉怎么做的？",
          "az": "是盘煎的，先生。",
          "key": "pan-fried",
          "keyz": "盘煎",
          "variants": [
            "How do you cook the steak?",
            "Is it fried or grilled?"
          ],
          "accept": [
            [
              "pan fried",
              "panfried",
              "pan-fried"
            ]
          ],
          "samples": [
            "It's pan-fried with red wine sauce.",
            "The beef is pan-fried."
          ]
        },
        {
          "w": "grilled",
          "wz": "烤（炙烤）",
          "s": "The chicken is grilled with herbs.",
          "sz": "鸡肉是香草炙烤的。",
          "q": "How is the chicken cooked?",
          "a": "It is grilled with herbs.",
          "qz": "鸡肉怎么做的？",
          "az": "香草炙烤。",
          "key": "grilled",
          "keyz": "炙烤",
          "variants": [
            "Is the chicken grilled?",
            "How do you prepare the chicken?"
          ],
          "accept": [
            [
              "grilled",
              "grill"
            ]
          ],
          "samples": [
            "The chicken is grilled.",
            "We grill it with fresh herbs."
          ]
        },
        {
          "w": "beef",
          "wz": "牛肉",
          "s": "The beef is from Australia.",
          "sz": "牛肉来自澳大利亚。",
          "q": "Where is the beef from?",
          "a": "The beef is from Australia, sir.",
          "qz": "牛肉哪里产的？",
          "az": "澳大利亚，先生。",
          "key": "beef",
          "keyz": "牛肉",
          "variants": [
            "What kind of meat is it?",
            "Is the beef Australian?"
          ],
          "accept": [
            [
              "beef"
            ],
            [
              "australia",
              "australian"
            ]
          ],
          "samples": [
            "It's Australian beef.",
            "The beef comes from Australia."
          ]
        },
        {
          "w": "lamb",
          "wz": "羔羊肉",
          "s": "We also have lamb for the main course.",
          "sz": "主菜也有羔羊肉。",
          "q": "Do you have lamb?",
          "a": "Yes, we have lamb rack.",
          "qz": "有羊肉吗？",
          "az": "有，羊脊排。",
          "key": "lamb",
          "keyz": "羔羊肉",
          "variants": [
            "Is lamb available?",
            "Any lamb on the menu?"
          ],
          "accept": [
            [
              "lamb"
            ]
          ],
          "samples": [
            "Yes, we serve lamb cutlet.",
            "Lamb is available today."
          ]
        },
        {
          "w": "seafood",
          "wz": "海鲜",
          "s": "White wine goes well with seafood.",
          "sz": "白葡萄酒很配海鲜。",
          "q": "What wine goes with seafood?",
          "a": "A white wine for seafood, Sauvignon Blanc.",
          "qz": "海鲜配什么酒？",
          "az": "白葡萄酒，长相思。",
          "key": "seafood",
          "keyz": "海鲜",
          "variants": [
            "Which wine pairs with fish?",
            "What should I drink with seafood?"
          ],
          "accept": [
            [
              "white wine"
            ],
            [
              "sauvignon blanc",
              "sauvignon"
            ]
          ],
          "samples": [
            "I'd suggest a white wine for seafood.",
            "The Sauvignon Blanc matches seafood well."
          ]
        },
        {
          "w": "abalone",
          "wz": "鲍鱼",
          "s": "The prawn and abalone comes with udon.",
          "sz": "鲍鱼虾仁配乌冬面。",
          "q": "What is in the second main course?",
          "a": "Prawn and abalone with udon noodles.",
          "qz": "第二道主菜是什么？",
          "az": "鲍鱼虾仁配乌冬面。",
          "key": "abalone",
          "keyz": "鲍鱼",
          "variants": [
            "Tell me about the second choice.",
            "What is the udon dish?"
          ],
          "accept": [
            [
              "abalone"
            ],
            [
              "prawn",
              "shrimp"
            ],
            [
              "udon"
            ]
          ],
          "samples": [
            "It's stir-fried prawn and abalone with udon.",
            "The second choice has prawn and abalone."
          ]
        }
      ]
    },
    {
      "id": "side",
      "icon": "🧀",
      "name": "佐餐",
      "desc": "芝士、面包与色拉浇汁",
      "pairs": [
        {
          "w": "Brie",
          "wz": "布里芝士（软身）",
          "s": "The French Brie is creamy and mild.",
          "sz": "法国布里芝士柔滑温和。",
          "q": "Which soft cheese do you recommend?",
          "a": "I'd recommend the French Brie.",
          "qz": "软身芝士推荐哪种？",
          "az": "我推荐法国布里。",
          "key": "Brie",
          "keyz": "布里芝士",
          "variants": [
            "What soft cheese do you have?",
            "Is Brie available?"
          ],
          "accept": [
            [
              "brie"
            ],
            [
              "creamy",
              "soft"
            ]
          ],
          "samples": [
            "The Brie is creamy and mild.",
            "May I suggest the French Brie?"
          ]
        },
        {
          "w": "Cheddar",
          "wz": "车达芝士（硬身）",
          "s": "British Cheddar is a hard cheese.",
          "sz": "英国车达是硬身芝士。",
          "q": "Which hard cheese do you have?",
          "a": "We have British Cheddar and Gruyere.",
          "qz": "有什么硬身芝士？",
          "az": "英国车达和瑞士古老也。",
          "key": "Cheddar",
          "keyz": "车达芝士",
          "variants": [
            "Do you have Cheddar?",
            "What hard cheese is available?"
          ],
          "accept": [
            [
              "cheddar"
            ],
            [
              "gruyere"
            ]
          ],
          "samples": [
            "British Cheddar and Swiss Gruyere.",
            "We have Cheddar from Britain."
          ]
        },
        {
          "w": "Danish Blue",
          "wz": "丹麦蓝芝士（松碎）",
          "s": "Danish Blue is a crumbly cheese.",
          "sz": "丹麦蓝是松碎芝士。",
          "q": "Do you have blue cheese?",
          "a": "Yes, we have Danish Blue.",
          "qz": "有蓝纹芝士吗？",
          "az": "有，丹麦蓝。",
          "key": "Danish Blue",
          "keyz": "丹麦蓝芝士",
          "variants": [
            "Is there any blue cheese?",
            "What crumbly cheese do you have?"
          ],
          "accept": [
            [
              "danish blue",
              "danishblue",
              "blue"
            ]
          ],
          "samples": [
            "We have Danish Blue for crumbly cheese.",
            "Yes, Danish Blue is available."
          ]
        },
        {
          "w": "rye roll",
          "wz": "黑麦面包",
          "s": "Would you like a rye roll?",
          "sz": "您要黑麦面包吗？",
          "q": "Can I have some bread?",
          "a": "Certainly, would you like a rye roll?",
          "qz": "能给我些面包吗？",
          "az": "当然，您要黑麦面包吗？",
          "key": "rye roll",
          "keyz": "黑麦面包",
          "variants": [
            "Could I get some bread?",
            "Do you have any bread?"
          ],
          "accept": [
            [
              "rye roll",
              "rye"
            ]
          ],
          "samples": [
            "We have rye roll and sesame bread.",
            "May I suggest the rye roll, sir?"
          ]
        },
        {
          "w": "sesame bread",
          "wz": "芝麻面包",
          "s": "We have sesame bread and garlic slices.",
          "sz": "我们有芝麻面包和蒜蓉面包。",
          "q": "What bread do you have?",
          "a": "Soft roll, rye roll and sesame bread.",
          "qz": "有什么面包？",
          "az": "软包、黑麦包和芝麻包。",
          "key": "sesame bread",
          "keyz": "芝麻面包",
          "variants": [
            "Which kinds of bread are there?",
            "Any sesame bread?"
          ],
          "accept": [
            [
              "sesame bread",
              "sesame"
            ],
            [
              "soft roll",
              "hard roll"
            ]
          ],
          "samples": [
            "We have soft roll, hard roll and sesame bread.",
            "Sesame bread is available."
          ]
        },
        {
          "w": "dressing",
          "wz": "色拉浇汁",
          "s": "We have thousand island dressing.",
          "sz": "我们有千岛酱。",
          "q": "I'd like the salad, please.",
          "a": "Thousand island or Italian dressing, sir?",
          "qz": "我要一份色拉，谢谢。",
          "az": "千岛酱还是意式酱，先生？",
          "key": "dressing",
          "keyz": "色拉浇汁",
          "variants": [
            "Can I have a salad?",
            "I'll take the salad."
          ],
          "accept": [
            [
              "thousand island"
            ],
            [
              "french vinegar",
              "french"
            ],
            [
              "italian"
            ]
          ],
          "samples": [
            "We have French and Italian dressing.",
            "May I suggest the thousand island?"
          ]
        }
      ]
    },
    {
      "id": "dessert",
      "icon": "🍰",
      "name": "甜品小食",
      "desc": "蛋糕、冰淇淋、巧克力与坚果",
      "pairs": [
        {
          "w": "ice cream",
          "wz": "冰淇淋",
          "s": "For dessert we have ice cream.",
          "sz": "甜品有冰淇淋。",
          "q": "What dessert do you have?",
          "a": "Ice cream and coconut cake.",
          "qz": "有什么甜品？",
          "az": "冰淇淋和椰子蛋糕。",
          "key": "ice cream",
          "keyz": "冰淇淋",
          "variants": [
            "What is for dessert?",
            "Any ice cream?"
          ],
          "accept": [
            [
              "ice cream",
              "icecream"
            ],
            [
              "coconut cake",
              "cake"
            ]
          ],
          "samples": [
            "We have coconut cake or ice cream.",
            "Ice cream is available."
          ]
        },
        {
          "w": "vanilla",
          "wz": "香草（口味）",
          "s": "Which flavor, vanilla or strawberry?",
          "sz": "什么口味，香草还是草莓？",
          "q": "What ice cream do you have?",
          "a": "We have vanilla and strawberry, sir.",
          "qz": "有什么冰淇淋？",
          "az": "有香草和草莓，先生。",
          "key": "vanilla",
          "keyz": "香草",
          "variants": [
            "Which ice cream flavors are there?",
            "Is vanilla available?"
          ],
          "accept": [
            [
              "vanilla"
            ]
          ],
          "samples": [
            "Vanilla and chocolate are available.",
            "May I suggest the vanilla, sir?"
          ]
        },
        {
          "w": "coconut cake",
          "wz": "椰子蛋糕",
          "s": "The coconut cake is very popular.",
          "sz": "椰子蛋糕很受欢迎。",
          "q": "What cake do you have?",
          "a": "We have coconut cake.",
          "qz": "有什么蛋糕？",
          "az": "我们有椰子蛋糕。",
          "key": "coconut cake",
          "keyz": "椰子蛋糕",
          "variants": [
            "Is there coconut cake?",
            "Which cake is available?"
          ],
          "accept": [
            [
              "coconut cake",
              "coconut"
            ]
          ],
          "samples": [
            "We serve coconut cake.",
            "Coconut cake is our special today."
          ]
        },
        {
          "w": "chocolate",
          "wz": "巧克力",
          "s": "Would you care for some chocolate?",
          "sz": "您要巧克力吗？",
          "q": "Do you have any chocolate?",
          "a": "Yes, would you care for some chocolate?",
          "qz": "有巧克力吗？",
          "az": "有的，您要来点巧克力吗？",
          "key": "chocolate",
          "keyz": "巧克力",
          "variants": [
            "Is chocolate available?",
            "Can I have some chocolate?"
          ],
          "accept": [
            [
              "chocolate"
            ]
          ],
          "samples": [
            "We have chocolate after the meal.",
            "Chocolate is available, sir."
          ]
        },
        {
          "w": "cashew",
          "wz": "腰果",
          "s": "Here are your cashews and drink.",
          "sz": "这是您的腰果和饮料。",
          "q": "What nuts do you have?",
          "a": "We have cashews and almonds.",
          "qz": "有什么坚果？",
          "az": "腰果和杏仁。",
          "key": "cashew",
          "keyz": "腰果",
          "variants": [
            "Which nuts are available?",
            "Do you have cashews?"
          ],
          "accept": [
            [
              "cashew",
              "cashews"
            ],
            [
              "almond",
              "almonds"
            ]
          ],
          "samples": [
            "We serve cashews and almonds.",
            "The cashews are freshly roasted."
          ]
        },
        {
          "w": "almond",
          "wz": "杏仁",
          "s": "The almonds are freshly roasted.",
          "sz": "杏仁是现烤的。",
          "q": "Can I have some nuts?",
          "a": "Would you prefer almonds or cashews, sir?",
          "qz": "能给我点坚果吗？",
          "az": "您想要杏仁还是腰果，先生？",
          "key": "almond",
          "keyz": "杏仁",
          "variants": [
            "Could I get some nuts?",
            "What nuts do you have?"
          ],
          "accept": [
            [
              "almond",
              "almonds"
            ]
          ],
          "samples": [
            "We have almonds and cashews today.",
            "May I suggest the roasted almonds?"
          ]
        }
      ]
    },
    {
      "id": "cabin",
      "icon": "✈️",
      "name": "客舱服务",
      "desc": "登机、安放行李与机上设备",
      "pairs": [
        {
          "w": "hot towel",
          "wz": "热毛巾",
          "s": "Here is the hot towel for you.",
          "sz": "这是给您的热毛巾。",
          "q": "May I have a hot towel?",
          "a": "Here is your hot towel, sir.",
          "qz": "能给我热毛巾吗？",
          "az": "给您热毛巾，先生。",
          "key": "hot towel",
          "keyz": "热毛巾",
          "variants": [
            "Could I get a hot towel?",
            "Do you have hot towels?"
          ],
          "accept": [
            [
              "hot towel",
              "towel"
            ]
          ],
          "samples": [
            "Here you are, a hot towel.",
            "Certainly, here is your hot towel."
          ]
        },
        {
          "w": "blanket",
          "wz": "毛毯",
          "s": "Let me get another blanket for you.",
          "sz": "我再给您拿一条毛毯。",
          "q": "Could I have a blanket?",
          "a": "Certainly, here is a blanket.",
          "qz": "能给我毛毯吗？",
          "az": "当然，给您毛毯。",
          "key": "blanket",
          "keyz": "毛毯",
          "variants": [
            "May I have one more blanket?",
            "Do you have a blanket?"
          ],
          "accept": [
            [
              "blanket"
            ]
          ],
          "samples": [
            "Of course, I'll bring a blanket.",
            "Here is an extra blanket for you."
          ]
        },
        {
          "w": "boarding pass",
          "wz": "登机牌",
          "s": "May I see your boarding pass?",
          "sz": "能看下您的登机牌吗？",
          "q": "Where is my seat?",
          "a": "May I see your boarding pass, please?",
          "qz": "我的座位在哪？",
          "az": "能看下您的登机牌吗？",
          "key": "boarding pass",
          "keyz": "登机牌",
          "variants": [
            "Can you help me find my seat?",
            "Which seat is mine?"
          ],
          "accept": [
            [
              "boarding pass"
            ],
            [
              "seat"
            ]
          ],
          "samples": [
            "Could I check your boarding pass?",
            "Your seat number is on the boarding pass."
          ]
        },
        {
          "w": "overhead locker",
          "wz": "头顶行李架",
          "s": "Your bag goes in the overhead locker.",
          "sz": "您的包放头顶行李架。",
          "q": "Where can I put my bag?",
          "a": "In the overhead locker, please.",
          "qz": "我的包放哪？",
          "az": "请放头顶行李架。",
          "key": "overhead locker",
          "keyz": "头顶行李架",
          "variants": [
            "Where should I stow my luggage?",
            "Can I keep my bag here?"
          ],
          "accept": [
            [
              "overhead locker",
              "overhead",
              "locker"
            ]
          ],
          "samples": [
            "Please stow it in the overhead locker.",
            "You may put it in the overhead compartment."
          ]
        },
        {
          "w": "lavatory",
          "wz": "洗手间",
          "s": "The lavatory is at the front.",
          "sz": "洗手间在前部。",
          "q": "Where is the lavatory?",
          "a": "The lavatory is at the front, sir.",
          "qz": "洗手间在哪？",
          "az": "在前部，先生。",
          "key": "lavatory",
          "keyz": "洗手间",
          "variants": [
            "Where is the restroom?",
            "Can you show me the toilet?"
          ],
          "accept": [
            [
              "lavatory",
              "restroom"
            ],
            [
              "front",
              "rear"
            ]
          ],
          "samples": [
            "It's at the front of the cabin.",
            "It's just ahead on your left."
          ]
        },
        {
          "w": "seatbelt",
          "wz": "安全带",
          "s": "Please fasten your seatbelt.",
          "sz": "请系好安全带。",
          "q": "Should I keep my seatbelt on?",
          "a": "Yes, please fasten your seatbelt.",
          "qz": "要一直系安全带吗？",
          "az": "是的，请系好安全带。",
          "key": "seatbelt",
          "keyz": "安全带",
          "variants": [
            "Do I need the seatbelt now?",
            "Must I wear the seatbelt?"
          ],
          "accept": [
            [
              "seatbelt",
              "seat belt"
            ],
            [
              "fasten"
            ]
          ],
          "samples": [
            "Please keep your seatbelt fastened.",
            "Yes, fasten it during the flight."
          ]
        }
      ]
    },
    {
      "id": "phrase",
      "icon": "💬",
      "name": "服务常用语",
      "desc": "高频应急与礼貌应答单句",
      "pairs": [
        {
          "w": "I am sorry about that",
          "wz": "对此我很抱歉",
          "s": "I am sorry about that, sir.",
          "sz": "对此我很抱歉，先生。",
          "q": "The meal is cold.",
          "a": "I am sorry about that, sir.",
          "qz": "餐食是凉的。",
          "az": "对此我很抱歉，先生。",
          "key": "sorry",
          "keyz": "抱歉",
          "variants": [
            "This is not what I ordered.",
            "I'm not happy with this."
          ],
          "accept": [
            [
              "sorry",
              "apologize"
            ]
          ],
          "samples": [
            "I do apologize for that.",
            "I'm terribly sorry about the inconvenience."
          ]
        },
        {
          "w": "Could you repeat that",
          "wz": "能请您重复一遍吗",
          "s": "Could you repeat that, please?",
          "sz": "能请您重复一遍吗？",
          "q": "I'd like the, um, the beef I think.",
          "a": "Could you repeat that, please?",
          "qz": "我要那个，嗯，牛肉吧。",
          "az": "能请您重复一遍吗？",
          "key": "repeat",
          "keyz": "重复",
          "variants": [
            "The chicken, no wait, the fish.",
            "Can I get, you know, that one?"
          ],
          "accept": [
            [
              "repeat",
              "pardon",
              "again"
            ]
          ],
          "samples": [
            "Sorry, could you say that again?",
            "Pardon me, could you repeat it?"
          ]
        },
        {
          "w": "Just a moment",
          "wz": "请稍等",
          "s": "Just a moment, please.",
          "sz": "请稍等。",
          "q": "Can I get my coat now?",
          "a": "Just a moment, please.",
          "qz": "现在能拿我的外套吗？",
          "az": "请稍等。",
          "key": "moment",
          "keyz": "稍等",
          "variants": [
            "Are you ready?",
            "Can you help me now?"
          ],
          "accept": [
            [
              "moment",
              "minute",
              "second"
            ]
          ],
          "samples": [
            "One moment, please.",
            "Please wait a moment."
          ]
        },
        {
          "w": "May I help you",
          "wz": "需要帮忙吗",
          "s": "May I help you with your luggage?",
          "sz": "需要我帮您拿行李吗？",
          "q": "(Passenger looks lost)",
          "a": "May I help you, sir?",
          "qz": "（旅客看起来在找东西）",
          "az": "需要帮忙吗，先生？",
          "key": "help",
          "keyz": "帮忙",
          "variants": [
            "I can't find my seat.",
            "Excuse me, miss?"
          ],
          "accept": [
            [
              "help",
              "assist"
            ]
          ],
          "samples": [
            "Can I help you with that?",
            "Let me help you, sir."
          ]
        },
        {
          "w": "You are welcome",
          "wz": "不客气",
          "s": "You are welcome, sir.",
          "sz": "不客气，先生。",
          "q": "Thank you so much.",
          "a": "You are welcome.",
          "qz": "太感谢了。",
          "az": "不客气。",
          "key": "welcome",
          "keyz": "不客气",
          "variants": [
            "Thanks a lot.",
            "I really appreciate it."
          ],
          "accept": [
            [
              "welcome",
              "pleasure"
            ]
          ],
          "samples": [
            "It's my pleasure.",
            "You're very welcome."
          ]
        },
        {
          "w": "Thank you for your understanding",
          "wz": "感谢您的理解",
          "s": "Thank you for your understanding.",
          "sz": "感谢您的理解。",
          "q": "(Passenger accepts the apology)",
          "a": "Thank you for your understanding.",
          "qz": "（旅客接受了道歉）",
          "az": "感谢您的理解。",
          "key": "understanding",
          "keyz": "理解",
          "variants": [
            "Alright, I understand.",
            "Fine, thank you."
          ],
          "accept": [
            [
              "thank you"
            ],
            [
              "understanding"
            ]
          ],
          "samples": [
            "Thanks for your understanding.",
            "I appreciate your understanding."
          ]
        }
      ]
    }
  ]
};
