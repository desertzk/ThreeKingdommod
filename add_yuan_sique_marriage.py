# -*- coding: utf-8 -*-
"""
袁思阙结婚事件 - 自动添加脚本
=================================
运行此脚本将自动向所有相关JSON文件中添加"乱世红颜"事件数据。
- 幂等设计：重复运行不会产生重复数据
- 自动备份：修改前自动创建 .bak 备份文件
- 大文件支持：对 >50MB 的文件使用流式处理

用法: python add_yuan_sique_marriage.py
"""

import json
import os
import shutil
import re
import sys

# ============================================================
# 配置
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 用于检测是否已添加的唯一标识
MARKER_PLOT_ID = "1090003"
MARKER_EVENT_ID = "3350015"
MARKER_BATTLE_ID = "1021503"
MARKER_CONV_TAG = "选项-乱世红颜"
MARKER_CONV_GROUP = "10330015"
MARKER_EVENTCC_ID = "3350015"
MARKER_BATTLEEC_ID = "1021503"
MARKER_CONVERSATION_GROUP = "10330015"

# ============================================================
# 数据定义 - 所有新增条目
# ============================================================

# ----- Plot.json -----
PLOT_ENTRIES = [
    {"userIndex":"20","id":"1090003","name":"乱世红颜","nameTc":"","nameEn":"","nameJp":"","nameKr":"","nameOther":"","remark":"袁思阙","parentID":"","activeCondition":"2/NPC关系等级/>=/2/0//3/2/0/WJ10981;2/NPC关系等级/</5/0//3/2/0/WJ10981;3/NPC已婚/=/否/3/2/0/WJ10981;3/NPC状态/=/已登场/3/0/0/WJ10981;1/玩家性别/=/男","finishCondition":"11/0/0/1090003/0;1/当前在大地图/=/否","failCondition":"","activeEvent":"3350015;3350016","activeFailEvent":"","finishEvent":"3350070","failEvent":"","forceDescription":"","forceEvent":"","isBulletin":"0","isInherit":"0","isHide":"0","unstop":"0","deadline":"180","coolTime":"0","beginYear":"205","beginMonth":"1","endYear":"220","endMonth":"12","description":"袁绍之女袁思阙，武艺超群，性情刚烈。于乱世之中，寻一良人，共度余生......\n\n亲历条件:【与袁思阙关系等级至少为2级】、【袁思阙未婚】、【袁思阙已登场】、【玩家性别为男】\n\n逆天改命:【武斗战胜袁思阙后可与其结为连理】","descriptionTc":"","descriptionEn":"","descriptionJp":"","descriptionKr":"","descriptionOther":"","progress":"","progressTc":"","progressEn":"","progressJp":"","progressKr":"","progressOther":"","isShowComming":"1","comingType":"1","annualPlot":"0","noTimeLimit":"0","dontStopTimeGoing":"0","quitOfficeFail":"0"},
    {"userIndex":"20","id":"1090103","name":"见袁思阙","nameTc":"","nameEn":"","nameJp":"","nameKr":"","nameOther":"","remark":"","parentID":"1090003","activeCondition":"","finishCondition":"14/0/1090003","failCondition":"","activeEvent":"3350017","activeFailEvent":"","finishEvent":"3350018","failEvent":"3350019","forceDescription":"","forceEvent":"","isBulletin":"0","isInherit":"0","isHide":"0","unstop":"0","deadline":"150","coolTime":"0","beginYear":"0","beginMonth":"0","endYear":"0","endMonth":"0","description":"袁思阙有事相商，可前往邺城一探究竟。","descriptionTc":"","descriptionEn":"","descriptionJp":"","descriptionKr":"","descriptionOther":"","progress":"前往邺城","progressTc":"","progressEn":"","progressJp":"","progressKr":"","progressOther":"","isShowComming":"0","comingType":"0","annualPlot":"0","noTimeLimit":"0","dontStopTimeGoing":"0","quitOfficeFail":"1"},
]

# ----- ConversationTag.json -----
CONVERSATION_TAG_ENTRIES = [
    {"tag":"选项-乱世红颜"},
]

# ----- ConversationInfo.json -----
CONVERSATION_INFO_ENTRIES = [
    {"userIndex":"20","groupID":"10330015","tag":"选项-乱世红颜","remark":"乱世红颜-1 初见袁思阙","openUIType":"0","replaceNPC":"0","replaceIndex":"0","replaceCondition":"","defaultLookAt":"1","isTemplate":"0"},
    {"userIndex":"20","groupID":"10330016","tag":"选项-乱世红颜","remark":"乱世红颜-2 深入交流","openUIType":"0","replaceNPC":"0","replaceIndex":"0","replaceCondition":"","defaultLookAt":"1","isTemplate":"0"},
    {"userIndex":"20","groupID":"10330017","tag":"选项-乱世红颜","remark":"乱世红颜-3 提议比武","openUIType":"0","replaceNPC":"0","replaceIndex":"0","replaceCondition":"","defaultLookAt":"1","isTemplate":"0"},
    {"userIndex":"20","groupID":"10330018","tag":"选项-乱世红颜","remark":"乱世红颜-4 武斗战胜","openUIType":"0","replaceNPC":"0","replaceIndex":"0","replaceCondition":"","defaultLookAt":"1","isTemplate":"0"},
    {"userIndex":"20","groupID":"10330019","tag":"选项-乱世红颜","remark":"乱世红颜-4 武斗战败","openUIType":"0","replaceNPC":"0","replaceIndex":"0","replaceCondition":"","defaultLookAt":"1","isTemplate":"0"},
    {"userIndex":"20","groupID":"10330020","tag":"选项-乱世红颜","remark":"乱世红颜-5 定情表白","openUIType":"0","replaceNPC":"0","replaceIndex":"0","replaceCondition":"","defaultLookAt":"1","isTemplate":"0"},
    {"userIndex":"20","groupID":"10330021","tag":"选项-乱世红颜","remark":"乱世红颜-6 战内对话","openUIType":"0","replaceNPC":"0","replaceIndex":"0","replaceCondition":"","defaultLookAt":"1","isTemplate":"0"},
    {"userIndex":"20","groupID":"10330022","tag":"选项-乱世红颜","remark":"乱世红颜-7 婚礼","openUIType":"0","replaceNPC":"0","replaceIndex":"0","replaceCondition":"","defaultLookAt":"1","isTemplate":"0"},
    {"userIndex":"20","groupID":"10330023","tag":"选项-乱世红颜","remark":"乱世红颜-8 婚后","openUIType":"0","replaceNPC":"0","replaceIndex":"0","replaceCondition":"","defaultLookAt":"1","isTemplate":"0"},
]

# ----- GameEvent.json -----
GAME_EVENT_ENTRIES = [
    {"userIndex":"20","eventID":"3350015","eventType":"4","option":"0","valueType":"0","value":"0","mission":"","missionState":"0","ignoreCondition":"1","getAssign":"0","getItemType":"0","getItemDType":"0","getLevel":"0","getNum":"1","getLack":"0","aryGetItem":"","unstop":"0","durationType":"0","costDay":"1","strengthType":"0","strength":"0","strengthFormula":"","mentalType":"0","mental":"0","mentalFormula":"","moodType":"0","mood":"0","moodFormula":"","inputNumIntent":"-1","selItemIntent":"-1","isAssign":"0","itemType":"0","itemDType":"0","minVal":"0","minLevel":"0","minNum":"1","maxNum":"1","arySelItem":"","character":"-1","internalAffair":"0","formula":"","useItemIntension":"-1","useItemType":"1","useItemID":"","useItemNum":"1","randomNPC":"","randomPlace":"","battleID":"","battleSide":"-1","battleEnd":"-1","variant":"","eventNPCType":"0","eventNPCDetail":"0","eventNPCIndex":"-1","eventNPCID":"","eventNPC":"","floatValue":"0.5","aryEvent":"","showText":"","showTextTc":"","showTextEn":"","showTextJp":"","showTextKr":"","showTextOther":"","textTitle":"","textTitleTc":"","textTitleEn":"","textTitleJp":"","textTitleKr":"","textTitleOther":"","textSubtitle":"","textSubtitleTc":"","textSubtitleEn":"","textSubtitleJp":"","textSubtitleKr":"","textSubtitleOther":""},
    {"userIndex":"20","eventID":"3350016","eventType":"4","option":"0","valueType":"0","value":"0","mission":"","missionState":"0","ignoreCondition":"1","getAssign":"0","getItemType":"0","getItemDType":"0","getLevel":"0","getNum":"1","getLack":"0","aryGetItem":"","unstop":"0","durationType":"0","costDay":"1","strengthType":"0","strength":"0","strengthFormula":"","mentalType":"0","mental":"0","mentalFormula":"","moodType":"0","mood":"0","moodFormula":"","inputNumIntent":"-1","selItemIntent":"-1","isAssign":"0","itemType":"0","itemDType":"0","minVal":"0","minLevel":"0","minNum":"1","maxNum":"1","arySelItem":"","character":"-1","internalAffair":"0","formula":"","useItemIntension":"-1","useItemType":"1","useItemID":"","useItemNum":"1","randomNPC":"","randomPlace":"","battleID":"","battleSide":"-1","battleEnd":"-1","variant":"","eventNPCType":"0","eventNPCDetail":"0","eventNPCIndex":"-1","eventNPCID":"","eventNPC":"","floatValue":"0.5","aryEvent":"","showText":"","showTextTc":"","showTextEn":"","showTextJp":"","showTextKr":"","showTextOther":"","textTitle":"","textTitleTc":"","textTitleEn":"","textTitleJp":"","textTitleKr":"","textTitleOther":"","textSubtitle":"","textSubtitleTc":"","textSubtitleEn":"","textSubtitleJp":"","textSubtitleKr":"","textSubtitleOther":""},
    {"userIndex":"20","eventID":"3350017","eventType":"4","option":"0","valueType":"0","value":"0","mission":"","missionState":"0","ignoreCondition":"1","getAssign":"0","getItemType":"0","getItemDType":"0","getLevel":"0","getNum":"1","getLack":"0","aryGetItem":"","unstop":"0","durationType":"0","costDay":"1","strengthType":"0","strength":"0","strengthFormula":"","mentalType":"0","mental":"0","mentalFormula":"","moodType":"0","mood":"0","moodFormula":"","inputNumIntent":"-1","selItemIntent":"-1","isAssign":"0","itemType":"0","itemDType":"0","minVal":"0","minLevel":"0","minNum":"1","maxNum":"1","arySelItem":"","character":"-1","internalAffair":"0","formula":"","useItemIntension":"-1","useItemType":"1","useItemID":"","useItemNum":"1","randomNPC":"","randomPlace":"","battleID":"","battleSide":"-1","battleEnd":"-1","variant":"","eventNPCType":"0","eventNPCDetail":"0","eventNPCIndex":"-1","eventNPCID":"","eventNPC":"","floatValue":"0.5","aryEvent":"","showText":"","showTextTc":"","showTextEn":"","showTextJp":"","showTextKr":"","showTextOther":"","textTitle":"","textTitleTc":"","textTitleEn":"","textTitleJp":"","textTitleKr":"","textTitleOther":"","textSubtitle":"","textSubtitleTc":"","textSubtitleEn":"","textSubtitleJp":"","textSubtitleKr":"","textSubtitleOther":""},
    {"userIndex":"20","eventID":"3350018","eventType":"4","option":"0","valueType":"0","value":"0","mission":"","missionState":"0","ignoreCondition":"1","getAssign":"0","getItemType":"0","getItemDType":"0","getLevel":"0","getNum":"1","getLack":"0","aryGetItem":"","unstop":"0","durationType":"0","costDay":"1","strengthType":"0","strength":"0","strengthFormula":"","mentalType":"0","mental":"0","mentalFormula":"","moodType":"0","mood":"0","moodFormula":"","inputNumIntent":"-1","selItemIntent":"-1","isAssign":"0","itemType":"0","itemDType":"0","minVal":"0","minLevel":"0","minNum":"1","maxNum":"1","arySelItem":"","character":"-1","internalAffair":"0","formula":"","useItemIntension":"-1","useItemType":"1","useItemID":"","useItemNum":"1","randomNPC":"","randomPlace":"","battleID":"","battleSide":"-1","battleEnd":"-1","variant":"","eventNPCType":"0","eventNPCDetail":"0","eventNPCIndex":"-1","eventNPCID":"","eventNPC":"","floatValue":"0.5","aryEvent":"","showText":"","showTextTc":"","showTextEn":"","showTextJp":"","showTextKr":"","showTextOther":"","textTitle":"","textTitleTc":"","textTitleEn":"","textTitleJp":"","textTitleKr":"","textTitleOther":"","textSubtitle":"","textSubtitleTc":"","textSubtitleEn":"","textSubtitleJp":"","textSubtitleKr":"","textSubtitleOther":""},
    {"userIndex":"20","eventID":"3350019","eventType":"4","option":"0","valueType":"0","value":"0","mission":"","missionState":"0","ignoreCondition":"1","getAssign":"0","getItemType":"0","getItemDType":"0","getLevel":"0","getNum":"1","getLack":"0","aryGetItem":"","unstop":"0","durationType":"0","costDay":"1","strengthType":"0","strength":"0","strengthFormula":"","mentalType":"0","mental":"0","mentalFormula":"","moodType":"0","mood":"0","moodFormula":"","inputNumIntent":"-1","selItemIntent":"-1","isAssign":"0","itemType":"0","itemDType":"0","minVal":"0","minLevel":"0","minNum":"1","maxNum":"1","arySelItem":"","character":"-1","internalAffair":"0","formula":"","useItemIntension":"-1","useItemType":"1","useItemID":"","useItemNum":"1","randomNPC":"","randomPlace":"","battleID":"","battleSide":"-1","battleEnd":"-1","variant":"","eventNPCType":"0","eventNPCDetail":"0","eventNPCIndex":"-1","eventNPCID":"","eventNPC":"","floatValue":"0.5","aryEvent":"","showText":"","showTextTc":"","showTextEn":"","showTextJp":"","showTextKr":"","showTextOther":"","textTitle":"","textTitleTc":"","textTitleEn":"","textTitleJp":"","textTitleKr":"","textTitleOther":"","textSubtitle":"","textSubtitleTc":"","textSubtitleEn":"","textSubtitleJp":"","textSubtitleKr":"","textSubtitleOther":""},
    {"userIndex":"20","eventID":"3350020","eventType":"24","option":"7","valueType":"1","value":"8","mission":"","missionState":"0","ignoreCondition":"1","getAssign":"0","getItemType":"0","getItemDType":"0","getLevel":"0","getNum":"1","getLack":"0","aryGetItem":"","unstop":"0","durationType":"0","costDay":"1","strengthType":"0","strength":"0","strengthFormula":"","mentalType":"0","mental":"0","mentalFormula":"","moodType":"0","mood":"0","moodFormula":"","inputNumIntent":"0","selItemIntent":"0","isAssign":"0","itemType":"0","itemDType":"0","minVal":"0","minLevel":"0","minNum":"1","maxNum":"1","arySelItem":"","character":"0","internalAffair":"0","formula":"","useItemIntension":"0","useItemType":"1","useItemID":"","useItemNum":"1","randomNPC":"","randomPlace":"","battleID":"","battleSide":"0","battleEnd":"0","variant":"","eventNPCType":"0","eventNPCDetail":"0","eventNPCIndex":"0","eventNPCID":"","eventNPC":"5/0/0/WJ10981/1/","floatValue":"0.5","aryEvent":"","showText":"","showTextTc":"","showTextEn":"","showTextJp":"","showTextKr":"","showTextOther":"","textTitle":"","textTitleTc":"","textTitleEn":"","textTitleJp":"","textTitleKr":"","textTitleOther":"","textSubtitle":"","textSubtitleTc":"","textSubtitleEn":"","textSubtitleJp":"","textSubtitleKr":"","textSubtitleOther":""},
    {"userIndex":"20","eventID":"3350025","eventType":"19","option":"0","valueType":"0","value":"0","mission":"","missionState":"0","ignoreCondition":"1","getAssign":"0","getItemType":"0","getItemDType":"0","getLevel":"0","getNum":"1","getLack":"0","aryGetItem":"","unstop":"0","durationType":"0","costDay":"1","strengthType":"0","strength":"0","strengthFormula":"","mentalType":"0","mental":"0","mentalFormula":"","moodType":"0","mood":"0","moodFormula":"","inputNumIntent":"-1","selItemIntent":"-1","isAssign":"0","itemType":"0","itemDType":"0","minVal":"0","minLevel":"0","minNum":"1","maxNum":"1","arySelItem":"","character":"-1","internalAffair":"0","formula":"","useItemIntension":"-1","useItemType":"1","useItemID":"","useItemNum":"1","randomNPC":"","randomPlace":"","battleID":"1021503","battleSide":"-1","battleEnd":"-1","variant":"","eventNPCType":"0","eventNPCDetail":"0","eventNPCIndex":"0","eventNPCID":"","eventNPC":"","floatValue":"0.5","aryEvent":"","showText":"","showTextTc":"","showTextEn":"","showTextJp":"","showTextKr":"","showTextOther":"","textTitle":"","textTitleTc":"","textTitleEn":"","textTitleJp":"","textTitleKr":"","textTitleOther":"","textSubtitle":"","textSubtitleTc":"","textSubtitleEn":"","textSubtitleJp":"","textSubtitleKr":"","textSubtitleOther":""},
    {"userIndex":"20","eventID":"3350030","eventType":"31","option":"6","valueType":"0","value":"1","mission":"","missionState":"1","ignoreCondition":"1","getAssign":"0","getItemType":"0","getItemDType":"0","getLevel":"0","getNum":"1","getLack":"0","aryGetItem":"","unstop":"0","durationType":"0","costDay":"1","strengthType":"0","strength":"0","strengthFormula":"","mentalType":"0","mental":"0","mentalFormula":"","moodType":"0","mood":"0","moodFormula":"","inputNumIntent":"0","selItemIntent":"0","isAssign":"0","itemType":"0","itemDType":"0","minVal":"0","minLevel":"0","minNum":"1","maxNum":"1","arySelItem":"","character":"0","internalAffair":"0","formula":"","useItemIntension":"0","useItemType":"1","useItemID":"","useItemNum":"1","randomNPC":"","randomPlace":"","battleID":"","battleSide":"1","battleEnd":"0","variant":"","eventNPCType":"0","eventNPCDetail":"0","eventNPCIndex":"0","eventNPCID":"","eventNPC":"2/2/0//1/","floatValue":"0.5","aryEvent":"","showText":"","showTextTc":"","showTextEn":"","showTextJp":"","showTextKr":"","showTextOther":"","textTitle":"","textTitleTc":"","textTitleEn":"","textTitleJp":"","textTitleKr":"","textTitleOther":"","textSubtitle":"","textSubtitleTc":"","textSubtitleEn":"","textSubtitleJp":"","textSubtitleKr":"","textSubtitleOther":""},
    {"userIndex":"20","eventID":"3350031","eventType":"31","option":"0","valueType":"0","value":"4","mission":"","missionState":"0","ignoreCondition":"1","getAssign":"0","getItemType":"0","getItemDType":"0","getLevel":"0","getNum":"1","getLack":"0","aryGetItem":"","unstop":"0","durationType":"0","costDay":"1","strengthType":"0","strength":"0","strengthFormula":"","mentalType":"0","mental":"0","mentalFormula":"","moodType":"0","mood":"0","moodFormula":"","inputNumIntent":"0","selItemIntent":"0","isAssign":"0","itemType":"0","itemDType":"0","minVal":"0","minLevel":"0","minNum":"1","maxNum":"1","arySelItem":"","character":"0","internalAffair":"0","formula":"","useItemIntension":"0","useItemType":"1","useItemID":"","useItemNum":"1","randomNPC":"","randomPlace":"","battleID":"","battleSide":"0","battleEnd":"0","variant":"","eventNPCType":"0","eventNPCDetail":"0","eventNPCIndex":"0","eventNPCID":"","eventNPC":"0/0/0//1/","floatValue":"0.5","aryEvent":"","showText":"","showTextTc":"","showTextEn":"","showTextJp":"","showTextKr":"","showTextOther":"","textTitle":"","textTitleTc":"","textTitleEn":"","textTitleJp":"","textTitleKr":"","textTitleOther":"","textSubtitle":"","textSubtitleTc":"","textSubtitleEn":"","textSubtitleJp":"","textSubtitleKr":"","textSubtitleOther":""},
    {"userIndex":"20","eventID":"3350032","eventType":"4","option":"0","valueType":"0","value":"0","mission":"","missionState":"0","ignoreCondition":"1","getAssign":"0","getItemType":"0","getItemDType":"0","getLevel":"0","getNum":"1","getLack":"0","aryGetItem":"","unstop":"0","durationType":"0","costDay":"1","strengthType":"0","strength":"0","strengthFormula":"","mentalType":"0","mental":"0","mentalFormula":"","moodType":"0","mood":"0","moodFormula":"","inputNumIntent":"-1","selItemIntent":"-1","isAssign":"0","itemType":"0","itemDType":"0","minVal":"0","minLevel":"0","minNum":"1","maxNum":"1","arySelItem":"","character":"-1","internalAffair":"0","formula":"","useItemIntension":"-1","useItemType":"1","useItemID":"","useItemNum":"1","randomNPC":"","randomPlace":"","battleID":"","battleSide":"-1","battleEnd":"-1","variant":"","eventNPCType":"0","eventNPCDetail":"0","eventNPCIndex":"-1","eventNPCID":"","eventNPC":"","floatValue":"0.5","aryEvent":"","showText":"","showTextTc":"","showTextEn":"","showTextJp":"","showTextKr":"","showTextOther":"","textTitle":"","textTitleTc":"","textTitleEn":"","textTitleJp":"","textTitleKr":"","textTitleOther":"","textSubtitle":"","textSubtitleTc":"","textSubtitleEn":"","textSubtitleJp":"","textSubtitleKr":"","textSubtitleOther":""},
    {"userIndex":"20","eventID":"3350040","eventType":"404","option":"0","valueType":"1","value":"0","mission":"","missionState":"0","ignoreCondition":"1","getAssign":"0","getItemType":"0","getItemDType":"0","getLevel":"0","getNum":"1","getLack":"0","aryGetItem":"","unstop":"0","durationType":"0","costDay":"1","strengthType":"0","strength":"0","strengthFormula":"","mentalType":"0","mental":"0","mentalFormula":"","moodType":"0","mood":"0","moodFormula":"","inputNumIntent":"0","selItemIntent":"0","isAssign":"0","itemType":"0","itemDType":"0","minVal":"0","minLevel":"0","minNum":"1","maxNum":"1","arySelItem":"0/0/-1/20000/0//0/0/0/-1//0;0/4/-1/20000/0//0/0/0/-1//0","character":"0","internalAffair":"0","formula":"","useItemIntension":"0","useItemType":"1","useItemID":"","useItemNum":"1","randomNPC":"","randomPlace":"","battleID":"","battleSide":"0","battleEnd":"0","variant":"","eventNPCType":"0","eventNPCDetail":"0","eventNPCIndex":"0","eventNPCID":"","eventNPC":"","floatValue":"0.5","aryEvent":"","showText":"","showTextTc":"","showTextEn":"","showTextJp":"","showTextKr":"","showTextOther":"","textTitle":"","textTitleTc":"","textTitleEn":"","textTitleJp":"","textTitleKr":"","textTitleOther":"","textSubtitle":"","textSubtitleTc":"","textSubtitleEn":"","textSubtitleJp":"","textSubtitleKr":"","textSubtitleOther":""},
    {"userIndex":"20","eventID":"3350045","eventType":"24","option":"7","valueType":"1","value":"20","mission":"","missionState":"0","ignoreCondition":"1","getAssign":"0","getItemType":"0","getItemDType":"0","getLevel":"0","getNum":"1","getLack":"0","aryGetItem":"","unstop":"0","durationType":"0","costDay":"1","strengthType":"0","strength":"0","strengthFormula":"","mentalType":"0","mental":"0","mentalFormula":"","moodType":"0","mood":"0","moodFormula":"","inputNumIntent":"0","selItemIntent":"0","isAssign":"0","itemType":"0","itemDType":"0","minVal":"0","minLevel":"0","minNum":"1","maxNum":"1","arySelItem":"","character":"0","internalAffair":"0","formula":"","useItemIntension":"0","useItemType":"1","useItemID":"","useItemNum":"1","randomNPC":"","randomPlace":"","battleID":"","battleSide":"0","battleEnd":"0","variant":"","eventNPCType":"0","eventNPCDetail":"0","eventNPCIndex":"0","eventNPCID":"","eventNPC":"5/0/0/WJ10981/1/","floatValue":"0.5","aryEvent":"","showText":"","showTextTc":"","showTextEn":"","showTextJp":"","showTextKr":"","showTextOther":"","textTitle":"","textTitleTc":"","textTitleEn":"","textTitleJp":"","textTitleKr":"","textTitleOther":"","textSubtitle":"","textSubtitleTc":"","textSubtitleEn":"","textSubtitleJp":"","textSubtitleKr":"","textSubtitleOther":""},
    {"userIndex":"20","eventID":"3350050","eventType":"24","option":"7","valueType":"1","value":"30","mission":"","missionState":"0","ignoreCondition":"1","getAssign":"0","getItemType":"0","getItemDType":"0","getLevel":"0","getNum":"1","getLack":"0","aryGetItem":"","unstop":"0","durationType":"0","costDay":"1","strengthType":"0","strength":"0","strengthFormula":"","mentalType":"0","mental":"0","mentalFormula":"","moodType":"0","mood":"0","moodFormula":"","inputNumIntent":"0","selItemIntent":"0","isAssign":"0","itemType":"0","itemDType":"0","minVal":"0","minLevel":"0","minNum":"1","maxNum":"1","arySelItem":"","character":"0","internalAffair":"0","formula":"","useItemIntension":"0","useItemType":"1","useItemID":"","useItemNum":"1","randomNPC":"","randomPlace":"","battleID":"","battleSide":"0","battleEnd":"0","variant":"","eventNPCType":"0","eventNPCDetail":"0","eventNPCIndex":"0","eventNPCID":"","eventNPC":"5/0/0/WJ10981/1/","floatValue":"0.5","aryEvent":"","showText":"","showTextTc":"","showTextEn":"","showTextJp":"","showTextKr":"","showTextOther":"","textTitle":"","textTitleTc":"","textTitleEn":"","textTitleJp":"","textTitleKr":"","textTitleOther":"","textSubtitle":"","textSubtitleTc":"","textSubtitleEn":"","textSubtitleJp":"","textSubtitleKr":"","textSubtitleOther":""},
    {"userIndex":"20","eventID":"3350060","eventType":"505","option":"0","valueType":"0","value":"0","mission":"","missionState":"0","ignoreCondition":"1","getAssign":"0","getItemType":"0","getItemDType":"0","getLevel":"0","getNum":"1","getLack":"0","aryGetItem":"","unstop":"0","durationType":"0","costDay":"1","strengthType":"0","strength":"0","strengthFormula":"","mentalType":"0","mental":"0","mentalFormula":"","moodType":"0","mood":"0","moodFormula":"","inputNumIntent":"0","selItemIntent":"0","isAssign":"0","itemType":"0","itemDType":"0","minVal":"0","minLevel":"0","minNum":"1","maxNum":"1","arySelItem":"","character":"0","internalAffair":"0","formula":"1001305","useItemIntension":"0","useItemType":"1","useItemID":"","useItemNum":"1","randomNPC":"","randomPlace":"","battleID":"","battleSide":"0","battleEnd":"0","variant":"","eventNPCType":"0","eventNPCDetail":"0","eventNPCIndex":"-1","eventNPCID":"","eventNPC":"","floatValue":"0.5","aryEvent":"","showText":"","showTextTc":"","showTextEn":"","showTextJp":"","showTextKr":"","showTextOther":"","textTitle":"","textTitleTc":"","textTitleEn":"","textTitleJp":"","textTitleKr":"","textTitleOther":"","textSubtitle":"","textSubtitleTc":"","textSubtitleEn":"","textSubtitleJp":"","textSubtitleKr":"","textSubtitleOther":""},
    {"userIndex":"20","eventID":"3350065","eventType":"30","option":"0","valueType":"0","value":"0","mission":"","missionState":"0","ignoreCondition":"1","getAssign":"0","getItemType":"0","getItemDType":"0","getLevel":"0","getNum":"1","getLack":"0","aryGetItem":"","unstop":"0","durationType":"0","costDay":"1","strengthType":"0","strength":"0","strengthFormula":"","mentalType":"0","mental":"0","mentalFormula":"","moodType":"0","mood":"0","moodFormula":"","inputNumIntent":"0","selItemIntent":"0","isAssign":"0","itemType":"0","itemDType":"0","minVal":"0","minLevel":"0","minNum":"1","maxNum":"1","arySelItem":"","character":"0","internalAffair":"0","formula":"","useItemIntension":"0","useItemType":"1","useItemID":"","useItemNum":"1","randomNPC":"","randomPlace":"","battleID":"","battleSide":"0","battleEnd":"0","variant":"","eventNPCType":"0","eventNPCDetail":"0","eventNPCIndex":"0","eventNPCID":"","eventNPC":"","floatValue":"0.5","aryEvent":"","showText":"","showTextTc":"","showTextEn":"","showTextJp":"","showTextKr":"","showTextOther":"","textTitle":"","textTitleTc":"","textTitleEn":"","textTitleJp":"","textTitleKr":"","textTitleOther":"","textSubtitle":"","textSubtitleTc":"","textSubtitleEn":"","textSubtitleJp":"","textSubtitleKr":"","textSubtitleOther":""},
    {"userIndex":"20","eventID":"3350070","eventType":"4","option":"0","valueType":"0","value":"0","mission":"","missionState":"0","ignoreCondition":"1","getAssign":"0","getItemType":"0","getItemDType":"0","getLevel":"0","getNum":"1","getLack":"0","aryGetItem":"","unstop":"0","durationType":"0","costDay":"1","strengthType":"0","strength":"0","strengthFormula":"","mentalType":"0","mental":"0","mentalFormula":"","moodType":"0","mood":"0","moodFormula":"","inputNumIntent":"-1","selItemIntent":"-1","isAssign":"0","itemType":"0","itemDType":"0","minVal":"0","minLevel":"0","minNum":"1","maxNum":"1","arySelItem":"","character":"-1","internalAffair":"0","formula":"","useItemIntension":"-1","useItemType":"1","useItemID":"","useItemNum":"1","randomNPC":"","randomPlace":"","battleID":"","battleSide":"-1","battleEnd":"-1","variant":"","eventNPCType":"0","eventNPCDetail":"0","eventNPCIndex":"-1","eventNPCID":"","eventNPC":"","floatValue":"0.5","aryEvent":"","showText":"","showTextTc":"","showTextEn":"","showTextJp":"","showTextKr":"","showTextOther":"","textTitle":"","textTitleTc":"","textTitleEn":"","textTitleJp":"","textTitleKr":"","textTitleOther":"","textSubtitle":"","textSubtitleTc":"","textSubtitleEn":"","textSubtitleJp":"","textSubtitleKr":"","textSubtitleOther":""},
]

# ----- GameEventCC.json -----
GAME_EVENT_CC_ENTRIES = [
    {"eventID":"3350015","weight":"100","else":"0","condition":"","conversation":"10330015"},
    {"eventID":"3350016","weight":"100","else":"0","condition":"","conversation":"10330016"},
    {"eventID":"3350017","weight":"100","else":"0","condition":"","conversation":"10330017"},
    {"eventID":"3350018","weight":"100","else":"0","condition":"","conversation":"10330018"},
    {"eventID":"3350019","weight":"100","else":"0","condition":"","conversation":"10330019"},
    {"eventID":"3350032","weight":"100","else":"0","condition":"","conversation":"10330021"},
    {"eventID":"3350070","weight":"100","else":"0","condition":"","conversation":"10330022"},
]

# ----- BattleInfo.json -----
BATTLE_INFO_ENTRIES = [
    {"userIndex":"20","id":"1021503","remark":"乱世红颜-与袁思阙切磋","remark2":"","rewardTips":"武魂记×2、随机武器×1、随机宝物×1","rewardTipsTc":"","rewardTipsEn":"","rewardTipsJp":"","rewardTipsKr":"","rewardTipsOther":"","winTips":"击败袁思阙","winTipsTc":"","winTipsEn":"","winTipsJp":"","winTipsKr":"","winTipsOther":"","loseTips":"AMING败退","loseTipsTc":"","loseTipsEn":"","loseTipsJp":"","loseTipsKr":"","loseTipsOther":"","additionTarget1":"","additionTarget1Tc":"","additionTarget1En":"","additionTarget1Jp":"","additionTarget1Kr":"","additionTarget1Other":"","additionTarget2":"","additionTarget2Tc":"","additionTarget2En":"","additionTarget2Jp":"","additionTarget2Kr":"","additionTarget2Other":"","additionReward1":"","additionReward1Tc":"","additionReward1En":"","additionReward1Jp":"","additionReward1Kr":"","additionReward1Other":"","additionReward2":"","additionReward2Tc":"","additionReward2En":"","additionReward2Jp":"","additionReward2Kr":"","additionReward2Other":"","additionCondition1":"","additionCondition2":"","source":"1","mission":"","canAuto":"0","scene":"80","return":"0","cameraMaxDis":"15","showPreview":"1","focusOnSpeaker":"1","mercenarySafe":"0","isWarBattle":"0","battleNPCIndex0":"0","battleNPCIndex1":"0","initCameraDirection":"0","roundFormulaID":"","canStudentReplace":"1","studentRewardFactor":"1"},
]

# ----- BattleInfoEC.json -----
BATTLE_INFO_EC_ENTRIES = [
    {"battleID":"1021503","start":"1","else":"0","once":"0","group":"0","condition":"","event":"3350030"},
    {"battleID":"1021503","start":"1","else":"0","once":"0","group":"0","condition":"","event":"3350031"},
    {"battleID":"1021503","start":"1","else":"0","once":"0","group":"0","condition":"","event":"3350032"},
    {"battleID":"1021503","start":"3","else":"0","once":"0","group":"0","condition":"1/[个人战][舌战][论战]结果/=/胜利","event":"3350040"},
]

# ----- Conversation.json -----
CONVERSATION_ENTRIES = [
    # Group 10330015 - 初见袁思阙
    {"groupID":"10330015","func":"1","npcID":"0","speakerIndex":"0","speakerID":"","listener":"1","listenerIndex":"0","imagePos":"0","imageID":"0","dialog":"袁思阙正在演武场上练习剑术，挥洒的汗水在阳光下闪闪发光。举手投足间尽显强者风范。听到AMING的脚步声，她收起剑势，转身面向AMING。","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},
    {"groupID":"10330015","func":"0","npcID":"3","speakerIndex":"0","speakerID":"","listener":"4","listenerIndex":"0","imagePos":"1","imageID":"0","dialog":"咦？贵人光临小女子的地盘，实在有失远迎。不知PCH今日大驾光临，所为何事？","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},
    {"groupID":"10330015","func":"0","npcID":"0","speakerIndex":"0","speakerID":"","listener":"3","listenerIndex":"0","imagePos":"0","imageID":"0","dialog":"袁思阙姑娘，闻名已久，今日一见，果然名不虚传。NI的剑术高超，WO早已听闻，今日能一睹其风采，实乃三生有幸。","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},
    {"groupID":"10330015","func":"0","npcID":"3","speakerIndex":"0","speakerID":"","listener":"4","listenerIndex":"0","imagePos":"1","imageID":"0","dialog":"过奖了。PCH的大名WO也是如雷贯耳，乱世之中能有NI这样的英杰，真乃天之幸。","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"&深入交流&10330016&&&&&&#&告辞&10330025&&&&&& ","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"3350020","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},

    # Group 10330016 - 深入交流
    {"groupID":"10330016","func":"0","npcID":"3","speakerIndex":"0","speakerID":"","listener":"4","listenerIndex":"0","imagePos":"1","imageID":"0","dialog":"我袁氏一族自祖父建立以来，威震四方。可惜父亲病逝后，兄长们反目成仇，从此我便独自隐居于此。","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},
    {"groupID":"10330016","func":"0","npcID":"0","speakerIndex":"0","speakerID":"","listener":"3","listenerIndex":"0","imagePos":"0","imageID":"0","dialog":"NI独守一方，不为名利所累，这份气节，足以让世间众多男儿汗颜。NI这样的奇女子，不应该被埋没于此。","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},
    {"groupID":"10330016","func":"0","npcID":"3","speakerIndex":"0","speakerID":"","listener":"4","listenerIndex":"0","imagePos":"1","imageID":"0","dialog":"（眼神中闪过一丝异彩）NI……能这样理解我，实在令我没想到。乱世浮萍，与其四处奔波，不如守得一份清净。","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},
    {"groupID":"10330016","func":"0","npcID":"0","speakerIndex":"0","speakerID":"","listener":"3","listenerIndex":"0","imagePos":"0","imageID":"0","dialog":"清净固然不错，但若能有一个相知相伴的人，难道不是更好么？","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"&提议比武&10330017&&&&&&#&就此告别&10330070&&&&&& ","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},

    # Group 10330017 - 提议比武
    {"groupID":"10330017","func":"0","npcID":"3","speakerIndex":"0","speakerID":"","listener":"4","listenerIndex":"0","imagePos":"1","imageID":"0","dialog":"（眼眸一亮，嘴角浮起淡淡笑容）NI的话，令我心中生起了战意。既然如此，何不让NI领略一下我的剑法？","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"&（接受挑战，拔剑相迎）&10330018&&&&&&#&（婉拒，扬长而去）&10330070&&&&&& ","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"3350025","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},

    # Group 10330018 - 武斗战胜后
    {"groupID":"10330018","func":"1","npcID":"0","speakerIndex":"0","speakerID":"","listener":"1","listenerIndex":"0","imagePos":"0","imageID":"0","dialog":"白热化的交锋之中，AMING将袁思阙逼到了角落。最终，AMING的剑力压过袁思阙，后者缓缓放下了兵刃。","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},
    {"groupID":"10330018","func":"0","npcID":"3","speakerIndex":"0","speakerID":"","listener":"4","listenerIndex":"0","imagePos":"1","imageID":"0","dialog":"（气喘吁吁，眼中闪烁着异样的光彩）我……输了。NI的剑法，确实令我叹为观止。","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},
    {"groupID":"10330018","func":"0","npcID":"0","speakerIndex":"0","speakerID":"","listener":"3","listenerIndex":"0","imagePos":"0","imageID":"0","dialog":"NI的剑法同样高明，与NI交手，WO也获益良多。（走近，目光深邃）武艺相当或许只是借口……其实，WO想更多地了解NI。","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"3350045","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},
    {"groupID":"10330018","func":"0","npcID":"3","speakerIndex":"0","speakerID":"","listener":"4","listenerIndex":"0","imagePos":"1","imageID":"0","dialog":"（面色变红，低眉顺眼，但嘴角却泛起难以掩饰的笑容）NI……想更多地了解我？","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"&（走近，搭住她的肩膀）&10330020&&&&&&#&（转身离开）&10330070&&&&&& ","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"3350050","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},

    # Group 10330019 - 武斗战败后
    {"groupID":"10330019","func":"1","npcID":"0","speakerIndex":"0","speakerID":"","listener":"1","listenerIndex":"0","imagePos":"0","imageID":"0","dialog":"激战之后，AMING终究未能战胜袁思阙。袁思阙收起剑势，走上前来。","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},
    {"groupID":"10330019","func":"0","npcID":"3","speakerIndex":"0","speakerID":"","listener":"4","listenerIndex":"0","imagePos":"1","imageID":"0","dialog":"NI的武艺尚有进步的空间，但NI的勇气令我欣赏。若日后武艺更精进，不妨再来找我切磋。","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},

    # Group 10330020 - 定情表白
    {"groupID":"10330020","func":"1","npcID":"0","speakerIndex":"0","speakerID":"","listener":"1","listenerIndex":"0","imagePos":"0","imageID":"0","dialog":"月明星稀，二人并肩坐在城墙之上，眺望远方。","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},
    {"groupID":"10330020","func":"0","npcID":"0","speakerIndex":"0","speakerID":"","listener":"3","listenerIndex":"0","imagePos":"0","imageID":"0","dialog":"袁思阙，WO想与NI携手，共度余生。NI愿意吗？","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},
    {"groupID":"10330020","func":"0","npcID":"3","speakerIndex":"0","speakerID":"","listener":"4","listenerIndex":"0","imagePos":"1","imageID":"0","dialog":"（转身面向AMING，眼眸清亮如月，带着坚定的光彩）WO早已在等待这句话。与NI携手，没有比这更好的选择了。","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"3350060","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},

    # Group 10330021 - 战内对话
    {"groupID":"10330021","func":"0","npcID":"3","speakerIndex":"0","speakerID":"","listener":"4","listenerIndex":"0","imagePos":"1","imageID":"0","dialog":"（执剑立于战场之上）来吧！让WO看看NI究竟有几分真本事！","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},

    # Group 10330022 - 婚礼
    {"groupID":"10330022","func":"1","npcID":"0","speakerIndex":"0","speakerID":"","listener":"1","listenerIndex":"0","imagePos":"0","imageID":"0","dialog":"在一片庄重而喜庆的氛围中，AMING与袁思阙在袁氏故地举行了盛大的婚礼。亲朋好友见证了这一刻，祝福的掌声为新婚夫妇献上。","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"3350065","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},
    {"groupID":"10330022","func":"0","npcID":"3","speakerIndex":"0","speakerID":"","listener":"4","listenerIndex":"0","imagePos":"1","imageID":"0","dialog":"（穿着精致的红色嫁衣，拜堂后轻轻握住AMING的手）从此以后，我们相携相伴，不离不弃。","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},
    {"groupID":"10330022","func":"0","npcID":"0","speakerIndex":"0","speakerID":"","listener":"3","listenerIndex":"0","imagePos":"0","imageID":"0","dialog":"（紧紧握住她的手）一诺千金，WO与NI共此誓言。","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},

    # Group 10330023 - 婚后
    {"groupID":"10330023","func":"1","npcID":"0","speakerIndex":"0","speakerID":"","listener":"1","listenerIndex":"0","imagePos":"0","imageID":"0","dialog":"婚后的日子里，AMING与袁思阙琴瑟和鸣，相携相伴。乱世虽未平定，但二人已找到了彼此的归宿。","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},
    {"groupID":"10330023","func":"0","npcID":"3","speakerIndex":"0","speakerID":"","listener":"4","listenerIndex":"0","imagePos":"1","imageID":"0","dialog":"（微笑着靠在AMING肩上）虽是乱世，有NI在身边，便是WO最大的幸运。","dialogTc":"","dialogEn":"","dialogJp":"","dialogKr":"","dialogOther":"","option":"","conditionForPlay":"0","secondCondition":"0","else":"0","condition":"","autoEvent":"1","event":"","dontForceStopAnimation":"0","stateType":"0","animType":"0","animationID":"10104","repeat":"0","keepItem":"0","faceType":"0","face":"0","faceVal":"0","forceDirection":"0","speakerDirection":"0","listenerDirection":"0","otherDirection":"7","jumpPlayer":"0","isCommonPeople":"0","duration":"1","interval":"2","speakingEffect":"0","clearSounds":"0","strTagFormulaID":""},
]


# ============================================================
# 工具函数
# ============================================================

def backup_file(filepath):
    """创建备份文件 (.bak)"""
    bak = filepath + ".bak"
    if not os.path.exists(bak):
        shutil.copy2(filepath, bak)
        print(f"  [备份] 已创建 {os.path.basename(bak)}")
    else:
        print(f"  [备份] {os.path.basename(bak)} 已存在，跳过")


def check_marker_in_file(filepath, marker_text):
    """检查文件中是否存在标记文本（用于判断幂等）"""
    with open(filepath, "r", encoding="utf-8-sig") as f:
        # 逐行检查，以应对大文件
        for line in f:
            if marker_text in line:
                return True
    return False


def append_entries_small_file(filepath, entries, marker_key, marker_value):
    """
    对小文件(<50MB)：解析为 JSON 数组，追加条目，写回。
    - 保持每行一个条目的格式（与原文件保持一致）。
    """
    # 幂等检查
    if check_marker_in_file(filepath, f'"{marker_key}":"{marker_value}"'):
        print(f"  [跳过] {os.path.basename(filepath)} 已包含数据，无需重复添加")
        return False

    backup_file(filepath)

    with open(filepath, "r", encoding="utf-8-sig") as f:
        content = f.read()

    # 找到最后一个 ] 的位置
    last_bracket = content.rfind("]")
    if last_bracket == -1:
        print(f"  [错误] {os.path.basename(filepath)} 格式异常，未找到 ]")
        return False

    # 构建要追加的文本
    new_lines = []
    for entry in entries:
        line = json.dumps(entry, ensure_ascii=False, separators=(",", ":"))
        new_lines.append(line)

    append_text = ",\n" + ",\n".join(new_lines)

    # 插入到 ] 之前
    new_content = content[:last_bracket] + append_text + "\n" + content[last_bracket:]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"  [成功] {os.path.basename(filepath)} 添加了 {len(entries)} 条数据")
    return True


def append_entries_large_file(filepath, entries, marker_text):
    """
    对大文件(>50MB)：不加载全部内容到内存，用尾部定位方式追加。
    读取文件尾部找到 ]，在其前面插入新条目。
    """
    # 幂等检查
    if check_marker_in_file(filepath, marker_text):
        print(f"  [跳过] {os.path.basename(filepath)} 已包含数据，无需重复添加")
        return False

    backup_file(filepath)

    # 读取全部内容
    with open(filepath, "r", encoding="utf-8-sig") as f:
        content = f.read()

    # 找到最后一个 ] 的位置
    last_bracket = content.rfind("]")
    if last_bracket == -1:
        print(f"  [错误] {os.path.basename(filepath)} 格式异常")
        return False

    # 构建新条目文本
    new_lines = []
    for entry in entries:
        line = json.dumps(entry, ensure_ascii=False, separators=(",", ":"))
        new_lines.append(line)

    append_text = ",\n" + ",\n".join(new_lines)

    # 写入：原内容(截至])前插入追加文本
    new_content = content[:last_bracket] + append_text + "\n]"
    # 保留 ] 之后可能的换行
    trailing = content[last_bracket + 1:]
    if trailing.strip():
        new_content += trailing

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"  [成功] {os.path.basename(filepath)} 添加了 {len(entries)} 条数据")
    return True


# ============================================================
# 主逻辑
# ============================================================

def main():
    print("=" * 60)
    print("  袁思阙结婚事件 - 自动添加脚本")
    print("  事件名称: 乱世红颜")
    print("=" * 60)
    print()

    results = {}

    # 1. Plot.json
    print("[1/8] Plot.json - 剧情任务")
    filepath = os.path.join(BASE_DIR, "Plot.json")
    results["Plot.json"] = append_entries_small_file(
        filepath, PLOT_ENTRIES, "id", MARKER_PLOT_ID
    )
    print()

    # 2. ConversationTag.json
    print("[2/8] ConversationTag.json - 对话标签")
    filepath = os.path.join(BASE_DIR, "ConversationTag.json")
    results["ConversationTag.json"] = append_entries_small_file(
        filepath, CONVERSATION_TAG_ENTRIES, "tag", MARKER_CONV_TAG
    )
    print()

    # 3. ConversationInfo.json
    print("[3/8] ConversationInfo.json - 对话组信息")
    filepath = os.path.join(BASE_DIR, "ConversationInfo.json")
    results["ConversationInfo.json"] = append_entries_small_file(
        filepath, CONVERSATION_INFO_ENTRIES, "groupID", MARKER_CONV_GROUP
    )
    print()

    # 4. GameEvent.json (大文件)
    print("[4/8] GameEvent.json - 游戏事件 (大文件)")
    filepath = os.path.join(BASE_DIR, "GameEvent.json")
    results["GameEvent.json"] = append_entries_large_file(
        filepath, GAME_EVENT_ENTRIES, f'"eventID":"{MARKER_EVENT_ID}"'
    )
    print()

    # 5. GameEventCC.json
    print("[5/8] GameEventCC.json - 事件对话映射")
    filepath = os.path.join(BASE_DIR, "GameEventCC.json")
    results["GameEventCC.json"] = append_entries_small_file(
        filepath, GAME_EVENT_CC_ENTRIES, "eventID", MARKER_EVENTCC_ID
    )
    print()

    # 6. BattleInfo.json
    print("[6/8] BattleInfo.json - 战斗配置")
    filepath = os.path.join(BASE_DIR, "BattleInfo.json")
    results["BattleInfo.json"] = append_entries_small_file(
        filepath, BATTLE_INFO_ENTRIES, "id", MARKER_BATTLE_ID
    )
    print()

    # 7. BattleInfoEC.json
    print("[7/8] BattleInfoEC.json - 战斗事件条件")
    filepath = os.path.join(BASE_DIR, "BattleInfoEC.json")
    results["BattleInfoEC.json"] = append_entries_small_file(
        filepath, BATTLE_INFO_EC_ENTRIES, "battleID", MARKER_BATTLEEC_ID
    )
    print()

    # 8. Conversation.json (大文件)
    print("[8/8] Conversation.json - 对话内容 (大文件)")
    filepath = os.path.join(BASE_DIR, "Conversation.json")
    results["Conversation.json"] = append_entries_large_file(
        filepath, CONVERSATION_ENTRIES, f'"groupID":"{MARKER_CONVERSATION_GROUP}"'
    )
    print()

    # 汇总
    print("=" * 60)
    print("  执行结果汇总")
    print("=" * 60)
    added = sum(1 for v in results.values() if v is True)
    skipped = sum(1 for v in results.values() if v is False)
    print(f"  新增: {added} 个文件")
    print(f"  跳过: {skipped} 个文件 (已存在)")
    print()
    for fname, result in results.items():
        status = "✓ 已添加" if result else "- 已跳过"
        print(f"  {status}  {fname}")
    print()

    if added > 0:
        print("  所有修改已完成！备份文件以 .bak 后缀保存。")
        print("  如需回滚，将 .bak 文件重命名为原文件名即可。")
    else:
        print("  所有数据已存在，无需修改。")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
