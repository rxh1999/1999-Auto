import plugins.mission_ready as mission_ready
import lib.find as f
import time
import lib.adb_command as adb
from config.config import data
import lib.ppocr as pp
import lib.api as api
import lib.utils as utils
import lib.const as const

IMAGE_RESOURCE = "imgs/active_resource"
IMAGE_SOMNAMBULISM = "imgs/active_somnambulism"
IMAGE_THE_POUSSIERE = 'imgs/level_poussiere'
"""经验"""
IMAGE_MINTAGE_AESTHETICS = 'imgs/level_mintage_aesthetics'
"""钱"""
IMAGE_HARVEST = 'imgs/level_harvest'
"""基建"""
IMAGE_ANALYSIS = 'imgs/level_analysis'
"""圣遗物狗粮"""
IMAGE_SOMNAMBULISM_ENTER = "imgs/level_somnambulism_enter"
"""进入人工梦境"""
IMAGE_SOMNAMBULISM_NEXT_BATTLE = "imgs/somnambulism_next_battle"
"""下一场人工梦境"""


REPLAY_1 = (0.63, 0.85)
"""复现1次"""
REPLAY_2 = (0.63, 0.76)
"""复现2次"""
REPLAY_3 = (0.63, 0.68)
"""复现3次"""
REPLAY_4 = (0.63, 0.59)
"""复现4次"""
LEVEL_4 = 4
"""第4关"""
LEVEL_5 = 5
"""第5关"""
LEVEL_6 = 6
"""第6关"""


IMAGE_START = "imgs/START_ACTIVE"
IMAGE_REPLAY = 'imgs/enter_replay_mode2'
IMAGE_REPLAY_SELECT = 'imgs/replay_select'
IMAGE_START_REPLAY = 'imgs/start_replay'
IMAGE_BATTLE_INFO = "imgs/battle_info"
IMAGE_BATTLE_INFO_RESTART = "imgs/battle_info_restart"
IMAGE_SOMNAMBULISM_RESET = "imgs/somnambulism_reset"

def Auto_Active(type: str, level: int, times ):
    """
    进入特定关卡进行复现.
    :param level:第几关.
    :param type:关卡类型.
    :param times:复现次数.
    """    
    if not mission_ready.ready():
        raise RuntimeError('无法返回主菜单')
    res=f.cut_find_html('imgs/enter_the_show',1162,175,1529,738)
    if res is None:
        x,y=f.cut_find_html('imgs/enter_the_show2',1162,175,1529,738)
    adb.touch([x,y+20])
    print("正在进入主会场")
    time.sleep(1)


    adb.touch(f.find(IMAGE_RESOURCE))
    print("点击资源")
    time.sleep(1)
    adb.touch(f.find(type))
    print(f"正在进入{type}")
    time.sleep(0.8)

    # level_click = f.find(level)
    # print(level_click)
    # if (level_click[2] < 0.6):
    #     adb.swipe((data['y']-100,data['x']/2),(100,data['x']/2))
    #     level_click = f.find(level)
    # adb.touch(level_click)
    to_level(level)
    print(f"正在进入{level}")
    time.sleep(0.8) 




    adb.touch(f.find(IMAGE_START))
    print(f"正在进入开始界面菜单")
    time.sleep(3.5)


    replay = f.find(IMAGE_REPLAY)
    print(replay)
    if replay[2] > 0.72:
        adb.touch(replay)
        print(f"选择复现模式")
    time.sleep(1.7)
    adb.touch(f.find(IMAGE_REPLAY_SELECT))
    print(f"选择复现次数")
    adb.touch((data['y'] * times[0], data['x'] * times[1]))

    adb.touch(f.find(IMAGE_START_REPLAY))
    print(f"开始复现")
    time.sleep(20)

    while(True):
        adb.touch((50,data['x']/2))
        time.sleep(3)
        ans = pp.ocr_bytes_xy(f.find_image(IMAGE_START_REPLAY))
        if (len(ans)>0):
            if ans[2] is not None and '复现' in ans[2]:
                break
    # time.sleep(3)
def to_level(level:int):
    for i in range(1,10):
        adb.swipe((1500,744),(200,750))
        time.sleep(0.1)
    for i in range(1,99):
        screen=api.get_scrren_shot_bytes()
        res=f.detect_numbers(screen)
        for num,xy in res:
            if num==level:
                x,y=xy
                y=y+50
                adb.touch([x+70,y+20])#输出坐标为数字左上角坐标，在此进行修正
                time.sleep(1)
                return True
        adb.swipe((100,744),(1040,750))
        time.sleep(1)
    return False
        

# Auto_Active(IMAGE_MINTAGE_AESTHEICS, LEVEL_6, REPLAY_4)

# TODO: 角色名补全，统一
def get_ally_image(ally):
    if "Bkornblume" == ally:
        return "imgs/team_select/bkornblume"

    if "Lilya" == ally:
        return "imgs/team_select/lilya"

    if "La_Source" == ally:
        return "imgs/team_select/la_source"

    if "Sputnik" == ally:
        return "imgs/team_select/sputnik"

    return ''


def team_formation(team):
    for ally in team:
        for _ in range(3):
            swip_top_to_bottom()
        ally_img = get_ally_image(ally)

        cnt = 10
        while(True):
            p = f.find(ally_img)
            if p[2] > 0.7:
                adb.touch(p)
                break
            else:
                swip_bottom_to_top()
                cnt -= 1
                if cnt <= 0:
                    break
        if cnt <= 0:
            raise "编队失败"
    adb.touch(f.find(const.IMAGE_CONFIRM))


def enter_somnambulism(team1, team2):
    if not mission_ready.ready():
        raise RuntimeError('无法返回主菜单')
    res = f.cut_find_html('imgs/enter_the_show', 1162, 175, 1529, 738)
    if res is None:
        x, y = f.cut_find_html('imgs/enter_the_show2', 1162, 175, 1529, 738)
    adb.touch([x, y + 20])
    print("正在进入主会场")
    time.sleep(1)

    adb.touch(f.find(IMAGE_SOMNAMBULISM))
    print("选择人工梦境")
    time.sleep(1)
    adb.touch(f.find(IMAGE_SOMNAMBULISM_ENTER))
    print("进入人工梦境")
    time.sleep(1)

    next_battle = None
    while True:
        next_battle = f.find(IMAGE_SOMNAMBULISM_NEXT_BATTLE)
        if next_battle is None or  next_battle[2] < 0.7:
            swip_right_to_left()
            continue
        else:
            break
    next_battle = (next_battle[0] - 100, next_battle[1] - 150)
    adb.touch(next_battle)
    print(f"正在进入人工梦境下一场战斗")

    if not utils.try_limited_sleep(0.5, lambda: f.find(IMAGE_SOMNAMBULISM_RESET)[2] > 0.7, 10):
        raise "进入人工梦境失败"

    api.get_screen_shot()
    loc = api.find_brightest_area()
    adb.touch(loc)
    if utils.try_limited_sleep(0.5, lambda: f.find(IMAGE_SOMNAMBULISM_RESET)[2] > 0.7, 10):
        raise "进入战斗失败"
    start = f.find(IMAGE_START)
    if start is None or start[2] <= 0.7:
        raise "进入战斗失败"

    # 选择队伍
    adb.touch((800, 300))
    time.sleep(1)

    adb.touch(f.find(const.IMAGE_QUICK_FORMATION))
    time.sleep(1)

    # TODO: 偶发识别失败
    find_and_touch(const.IMAGE_TEAM_1)
    find_and_touch(const.IMAGE_TEAM_2)
    find_and_touch(const.IMAGE_TEAM_3)
    find_and_touch(const.IMAGE_TEAM_4)

    if not team_formation(team1) and team_formation(team2):
        raise "无法完成编队"

    adb.touch(start)
    utils.try_limited(lambda: adb.touch((800, 10)), lambda: f.find(const.IMAGE_EMPTY_CARD)[2] > 0.8)


def find_and_touch(img:str):
    point = f.find(img)
    if point[2] > 0.6:
        adb.touch(point)

def swip_right_to_left():
    adb.swipe((1500, 744), (200, 750))

def swip_top_to_bottom():
    adb.swipe((855, 255), (855, 1000))

def swip_bottom_to_top():
    adb.swipe((855, 1000), (855, 255))